import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(__file__),'data', 'note_pal.db')

def init_db():
    if not os.path.exists(os.path.dirname(DB_PATH)):
        os.makedirs(os.path.dirname(DB_PATH))
        
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT NOT NULL,
            name TEXT NOT NULL,
            context TEXT NOT NULL CHECK (context IN ('work', 'personal', 'project')),
            status TEXT NOT NULL CHECK (status IN ('draft', 'done', 'delivered')),
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    c.execute('CREATE INDEX IF NOT EXISTS idx_notes_name ON notes(name);')
    c.execute('CREATE INDEX IF NOT EXISTS idx_notes_context ON notes(context);')
    c.execute('CREATE INDEX IF NOT EXISTS idx_notes_status ON notes(status);')
    
    conn.commit()
    conn.close()

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn