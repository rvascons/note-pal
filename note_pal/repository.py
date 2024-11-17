from datetime import datetime
from .database import init_db, get_db_connection

class NoteRepository:
    def __init__(self):
        init_db()
        self.conn = get_db_connection()
            
    def get_all(self, context_filter=None, status_filter=None, date_filter=None):
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
        if date_filter:
            conditions.append('created_at >= ?')
            params.append(date_filter.strftime('%Y-%m-%d %H:%M:%S'))
        if conditions:
            query += ' WHERE ' + ' AND '.join(conditions)
        query += ' ORDER BY created_at DESC'

        c.execute(query, params)
        return c.fetchall()

    def get_by_id(self, task_id):
        c = self.conn.cursor()
        c.execute('SELECT * FROM notes WHERE id = ?', (task_id,))
        return c.fetchone()
    
    def get_by_name(self, name):
        c = self.conn.cursor()
        c.execute('SELECT * FROM notes WHERE name = ?', (name,))
        return c.fetchone()

    def create(self, description, context, name, status = 'pending' ):
        if not name:
            name = datetime.now().isoformat()
    
        c = self.conn.cursor()
        c.execute('''
            INSERT INTO notes (description, context, name, status)
            VALUES (?, ?, ?, ?)
        ''', (description, context, name, status))
        self.conn.commit()

    def update(self, name, description, status, context, updated_at):
        c = self.conn.cursor()
        c.execute('''
            UPDATE notes
            SET description = ?, status = ?, context = ?, updated_at = ?
            WHERE name = ?
        ''', (description, status, context, updated_at, name))
        self.conn.commit()
        
    def delete(self, task_id):
        c = self.conn.cursor()
        c.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
        self.conn.commit()

    def mark_notes(self, date_before=None):
        c = self.conn.cursor()
        params = []
        query = '''
            UPDATE notes
            SET status = 'delivered', updated_at = ?
            WHERE status = 'pending'
        '''
        params.append(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        if date_before:
            query += ' AND created_at <= ?'
            params.append(date_before.strftime('%Y-%m-%d %H:%M:%S'))

        c.execute(query, params)
        self.conn.commit()
        return c.rowcount  # Returns the number of rows updated

    def close(self):
        self.conn.close()