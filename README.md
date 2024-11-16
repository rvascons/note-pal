# Note-Pal

Note-Pal is a Command Line Interface (CLI) application for managing notes directly from your terminal. It allows you to add, list, and organize notes with various options and filters. The project is built using Python and will be packaged using Poetry for easy distribution.

## Features

- **Add Notes**: Create new notes with descriptions, contexts, statuses, and optional names.
- **List Notes**: Display notes with filtering options by context and status.
- **Customizable Output**: Choose which fields to display when listing notes.
- **Data Storage**: Uses SQLite for efficient local data management.
- **Easy to Use**: Built with [Typer](https://typer.tiangolo.com/) for intuitive CLI commands.

## Installation

*Installation instructions will be provided once the package is published.*

## Usage

After installing Note-Pal, use the following commands:

### Add a Note
```bash
note-pal add "Description of your note" work --status draft --name "Optional Name"
```
- description: Description of the note.
- context: Context of the note (work, personal, project).
- --status, -s: (Optional) Status of the note (draft, done, delivered). Defaults to draft.
- --name, -n: (Optional) Name of the note. Defaults to the current timestamp.

### List Notes
```bash
note-pal list --context --status --filter-context work --filter-status draft
```
- --context, -c: Show the context in the output.
- --status, -s: Show the status in the output.
- --filter-context, -fc: Filter notes by context (work, personal, project).
- --filter-status, -fs: Filter notes by status (draft, done, delivered).

## Examples
**Add a New Note**
```bash
note-pal add "Finish the project documentation" work --name "Documentation Task"
```

***List All Notes Showing Context and Status***
```bash
note-pal list --context --status
```

***List Notes Filtered by Context***
```bash
note-pal list --filter-context personal
```

## Database
Note-Pal uses an SQLite database stored locally. The database is initialized automatically when you first run the application.

## Development
To set up the development environment:

1. Clone the Repository
```bash
git clone https://github.com/rvascons/note-pal.git
cd note-pal
```

2. Install Dependencies with Poetry
```bash
poetry install
```

3. Run the Application
```bash
poetry run note-pal --help
```

## Contributing
Contributions are welcome. Please open an issue or submit a pull request for any bugs or feature requests.

## License
This project is licensed under the MIT License.