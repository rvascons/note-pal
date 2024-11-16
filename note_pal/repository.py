from datetime import datetime
from .database import init_db, get_db_connection

class NoteRepository:
    def __init__(self):
        init_db()
        self.conn = get_db_connection()
            
    def get_all(self, context_filter=None, status_filter=None):
        c = self.conn.cursor()
        query = 'SELECT * FROM notes'
        params = []

        conditions = []
        if context_filter:
            conditions.append('context = ?')
            params.append(context_filter)
        if status_filter:
            conditions.append('status = ?')
            params.append(status_filter)
        if conditions:
            query += ' WHERE ' + ' AND '.join(conditions)

        c.execute(query, params)
        return c.fetchall()

    def get_by_id(self, task_id):
        c = self.conn.cursor()
        c.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
        return c.fetchone()

    def create(self, description, context, name, status = 'draft' ):
        if not name:
            name = datetime.now().isoformat()
            
        print(description, context, name, status)
        c = self.conn.cursor()
        c.execute('''
            INSERT INTO notes (description, context, name, status)
            VALUES (?, ?, ?, ?)
        ''', (description, context, name, status))
        self.conn.commit()

    def update(self, task_id, description, status, updated_at):
        c = self.conn.cursor()
        c.execute('''
            UPDATE tasks
            SET description = ?, status = ?, updated_at = ?
            WHERE id = ?
        ''', (description, status, updated_at, task_id))
        self.conn.commit()

    def delete(self, task_id):
        c = self.conn.cursor()
        c.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
        self.conn.commit()

    def close(self):
        self.conn.close()