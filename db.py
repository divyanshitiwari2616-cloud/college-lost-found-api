import sqlite3


class Database:

    def __init__(self, db_name="items.db"):
        self.db_name = db_name
        self.create_table()

    def connect(self):
        return sqlite3.connect(self.db_name)

    def create_table(self):

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                category TEXT NOT NULL,
                location TEXT NOT NULL,
                reported_by TEXT NOT NULL,
                status TEXT NOT NULL
            )
        """)

        conn.commit()
        conn.close()

    def create_item(self, item):

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO items
            (title, description, category, location, reported_by, status)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            item.title,
            item.description,
            item.category,
            item.location,
            item.reported_by,
            item.status
        ))

        item_id = cursor.lastrowid

        conn.commit()
        conn.close()

        return self.get_item(item_id)

    def get_items(self):

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, title, description, category,
                   location, reported_by, status
            FROM items
            ORDER BY id
        """)

        rows = cursor.fetchall()

        conn.close()

        return [
            {
                "id": row[0],
                "title": row[1],
                "description": row[2],
                "category": row[3],
                "location": row[4],
                "reported_by": row[5],
                "status": row[6]
            }
            for row in rows
        ]

    def get_item(self, item_id):

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, title, description, category,
                   location, reported_by, status
            FROM items
            WHERE id = ?
        """, (item_id,))

        row = cursor.fetchone()

        conn.close()

        if row is None:
            return None

        return {
            "id": row[0],
            "title": row[1],
            "description": row[2],
            "category": row[3],
            "location": row[4],
            "reported_by": row[5],
            "status": row[6]
        }

    def update_item(self, item_id, item):

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE items
            SET title = ?,
                description = ?,
                category = ?,
                location = ?,
                reported_by = ?,
                status = ?
            WHERE id = ?
        """, (
            item.title,
            item.description,
            item.category,
            item.location,
            item.reported_by,
            item.status,
            item_id
        ))

        updated = cursor.rowcount

        conn.commit()
        conn.close()

        if updated == 0:
            return None

        return self.get_item(item_id)

    def delete_item(self, item_id):

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM items
            WHERE id = ?
        """, (item_id,))

        deleted = cursor.rowcount

        conn.commit()
        conn.close()

        return deleted

    def get_items_by_status(self, status):

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, title, description, category,
                   location, reported_by, status
            FROM items
            WHERE LOWER(status) = LOWER(?)
            ORDER BY id
        """, (status,))

        rows = cursor.fetchall()

        conn.close()

        return [
            {
                "id": row[0],
                "title": row[1],
                "description": row[2],
                "category": row[3],
                "location": row[4],
                "reported_by": row[5],
                "status": row[6]
            }
            for row in rows
        ]

    def get_items_by_category(self, category):

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, title, description, category,
                   location, reported_by, status
            FROM items
            WHERE LOWER(category) = LOWER(?)
            ORDER BY id
        """, (category,))

        rows = cursor.fetchall()

        conn.close()

        return [
            {
                "id": row[0],
                "title": row[1],
                "description": row[2],
                "category": row[3],
                "location": row[4],
                "reported_by": row[5],
                "status": row[6]
            }
            for row in rows
        ]