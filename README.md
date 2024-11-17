# Note-Pal

Note-Pal is a Command Line Interface (CLI) application designed to help software engineers quickly capture and manage notes during their daily work. It was created to address the common issue of forgetting important activities or tasks that need to be reported in daily team meetings.

## Features

- **Quick Note Taking**: Instantly add notes with descriptions, contexts, statuses, and optional names.
- **Short-Term Focus**: Notes are intended to be temporary, serving as a reminder until the next daily meeting.
- **Tagging System**: Associate tags or contexts with notes to categorize them (e.g., work, personal, project).
- **Status Management**: Mark notes as done after they've been reported or addressed.
- **Summarization**: List and review notes to create a brief summary for daily reports.
- **Easy Reset**: After marking notes as done, start fresh for the next day.

## Installation

*Installation instructions will be provided once the package is published.*

## Usage

After installing Note-Pal, use the following commands:

### Add a Note
```bash
note-pal add "Fixed a critical bug in the authentication module" work --name "Auth Bug Fix"
```
- description: Description of the note.
- context: Context of the note (bug, feature, architecture, external, other).
- --status, -s: (Optional) Status of the note (pending, delivered). Defaults to pending.
- --name, -n: (Optional) Name of the note. Defaults to the current timestamp.

### List Notes
```bash
note-pal list --context --status --filter-context bug --time-frame "last day"
```
- --context, -c: Show the context in the output.
- --status, -s: Show the status in the output.
- --filter-context, -fc: Filter notes by context (bug, feature, architecture, external, other).
- --filter-status, -fs: Filter notes by status (pending, delivered).
- --time-frame, -t: Specify the time frame for listing notes ("last day", "last 7 days", "all time"). If not provided, it defaults to showing notes from all time with status pending.

### Mark Notes as Delivered
```bash
note-pal mark [DAYS]
```
- DAYS: (Optional) Number of days. Notes from N days ago and earlier will be marked as delivered.
If DAYS is not provided, all pending notes will be marked as delivered.

## Examples
**Add a New Note**
```bash
note-pal add "Finish the project documentation" work --name "Documentation Task"
```

**List Notes from the Last Day**
```bash
note-pal list --time-frame "last day"
```

***List All Pending Notes***
```bash
note-pal list
```

***List Notes Filtered by Context and Time Frame***
```bash
note-pal list --filter-context bug --time-frame "last 7 days"
```

***Mark All Notes as Delivered***
```bash
note-pal mark
```

***Mark notes from 2 days ago and earlier as delivered***
```bash
note-pal mark 2
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