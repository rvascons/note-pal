from datetime import datetime, timedelta
import typer
from .repository import NoteRepository
from rich.console import Console
from rich.table import Table
from rich.theme import Theme
from rich import box

app = typer.Typer()

custom_theme = Theme({
    "name": "bold magenta",
    "description": "yellow",
    "context": "cyan",
    "status": "green",
})
console = Console(theme=custom_theme)

@app.callback()
def init(ctx: typer.Context):
    ctx.obj = {}
    ctx.obj['repo'] = NoteRepository()

@app.command()
def list(
    ctx: typer.Context,
    show_context: bool = typer.Option(False, "--context", "-c", help="Show context in the output"),
    show_status: bool = typer.Option(False, "--status", "-s", help="Show status in the output"),
    filter_context: str = typer.Option(None, "--filter-context", "-fc", help="Filter notes by context"),
    filter_status: str = typer.Option(None, "--filter-status", "-fs", help="Filter notes by status"),
    time_frame: str = typer.Option(
        None,
        "--time-frame",
        "-t",
        help='Specify time frame ("last day", "last 7 days", "all time")'
    )
):
    """
    List all notes. By default, it lists all pending notes.
    """
    repo: NoteRepository = ctx.obj['repo']

    if time_frame is None and filter_status is None:
        filter_status = 'pending'
        time_frame = 'all time'

    date_filter = None
    if time_frame == 'last day':
        date_filter = datetime.now() - timedelta(days=1)
    elif time_frame == 'last 7 days':
        date_filter = datetime.now() - timedelta(days=7)
    elif time_frame == 'all time':
        date_filter = None
    else:
        console.print("[red]Invalid time frame specified. Use 'last day', 'last 7 days', or 'all time'.[/red]")
        raise typer.Exit()

    notes = repo.get_all(filter_context, filter_status, date_filter)

    if not notes:
        console.print("[yellow]No notes found[/yellow]")
        return

    table = Table(title="Notes", box=box.ROUNDED)

    table.add_column("Name", style="name", justify="left")
    table.add_column("Description", style="description", justify="left")
    if show_context:
        table.add_column("Context", style="context", justify="left")
    if show_status:
        table.add_column("Status", style="status", justify="left")

    for note in notes:
        row = [
            note['name'],
            note['description'],
        ]
        if show_context:
            row.append(note['context'])
        if show_status:
            row.append(note['status'])
        table.add_row(*row)

    console.print(table)

@app.command()
def add(
    ctx: typer.Context,
    description: str = typer.Argument(..., help="Description of the note"),
    context: str = typer.Argument(
        ...,
        help="Class of the note (bug, feature, architecture, external, other)"
    ),
    status: str = typer.Option(
        'pending',
        "--status",
        "-s",
        help="Status of the note (pending, delivered)(default: pending)"
    ),
    name: str = typer.Option(
        None,
        "--name",
        "-n",
        help="Name of the note (default: current timestamp)"
    )):
        
    """
    Add a new note.
    """
    repo: NoteRepository = ctx.obj['repo']
    repo.create(description, context, name, status)
    typer.echo("Note added successfully")

@app.command()
def update(
    ctx: typer.Context,
    name: str = typer.Argument(..., help="Name of the note to update"),
    description: str = typer.Option(None, "--description", "-d", help="New description for the note"),
    context: str = typer.Option(None, "--context", "-c", help="New context for the note"),
    status: str = typer.Option(None, "--status", "-s", help="New status for the note")
):
    """
    Update an existing note based on the name.
    """
    repo: NoteRepository = ctx.obj['repo']
    note = repo.get_by_name(name)
    if not note:
        typer.echo(f"Note with name '{name}' not found")
        raise typer.Exit(code=1)
    
    new_description = description if description is not None else note['description']
    new_status = status if status is not None else note['status']
    new_context = context if context is not None else note['context']

    repo.update(name, new_description, new_status, new_context, datetime.now())
    typer.echo(f"Note '{name}' updated successfully")

@app.command()
def mark(
    ctx: typer.Context,
    days: int = typer.Argument(
        None,
        help='Number of days. Notes from N days ago and earlier will be marked.'
    )
):
    """
    Mark pending notes as delivered based on the time frame (in days).

    Examples:

    - Mark all pending notes as delivered:
        note-pal mark

    - Mark notes from 2 days ago and earlier as delivered:
        note-pal mark 2

    If no days are specified, all pending notes will be marked as delivered.
    """
    repo: NoteRepository = ctx.obj['repo']

    date_before = None

    if days is not None:
        date_before = datetime.now() - timedelta(days=days)
        date_before = date_before.replace(hour=23, minute=59, second=59, microsecond=999999)

    updated_count = repo.mark_notes(date_before)
    if updated_count > 0:
        typer.echo(f"Marked {updated_count} note{'s' if updated_count != 1 else ''} as delivered.")
    else:
        typer.echo("No pending notes were found to mark.")

if __name__ == "__main__":
    app()