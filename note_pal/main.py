from calendar import c
import typer
from .repository import NoteRepository
app = typer.Typer()

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
    filter_status: str = typer.Option(None, "--filter-status", "-fs", help="Filter notes by status")
):
    """
    List all notes with optional filtering and output customization.
    """
    repo: NoteRepository = ctx.obj['repo']
    notes = repo.get_all(filter_context, filter_status)

    if not notes:
        typer.echo("No notes found")
        return

    # Determine the output format
    for note in notes:
        output = f"{note['name']}: {note['description']}"
        if show_context:
            output += f" - Context: {note['context']}"
        if show_status:
            output += f" - Status: {note['status']}"
        typer.echo(output)

@app.command()
def add(
    ctx: typer.Context,
    description: str = typer.Argument(..., help="Description of the note"),
    context: str = typer.Argument(
        ...,
        help="Class of the note (work, personal, project)"
    ),
    status: str = typer.Option(
        'draft',
        "--status",
        "-s",
        help="Status of the note (default: draft)"
    ),
    name: str = typer.Option(
        None,
        "--name",
        "-n",
        help="Name of the note (default: current timestamp)"
    )):
        
    """
    Add a new note
    """
    repo: NoteRepository = ctx.obj['repo']
    repo.create(description, context, name, status)
    typer.echo("Note added successfully")

if __name__ == "__main__":
    app()