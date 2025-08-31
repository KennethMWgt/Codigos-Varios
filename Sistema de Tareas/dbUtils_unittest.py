# dbUtils_unittest.py
import unittest
import sqlite3
from dbUtils import create_tables, insert_task, update_task, delete_task

class SQLiteTasksTestCase(unittest.TestCase):
    def setUp(self):
        self.conn = sqlite3.connect(":memory:")
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA foreign_keys = ON;")
        create_tables(self.conn)  

    def tearDown(self):
        self.conn.close()

    def fetch_all(self):
        cur = self.conn.execute("SELECT id, title, is_done, created_at FROM tasks ORDER BY id;")
        return cur.fetchall()

    def test_create_tables_is_idempotent(self):
        create_tables(self.conn) 
        tid = insert_task(self.conn, "First task")  
        self.assertIsInstance(tid, int)

    def test_insert_and_readback(self):
        tid = insert_task(self.conn, "Buy milk")
        rows = self.fetch_all()
        self.assertEqual(len(rows), 1)
        row = rows[0]
        self.assertEqual(row["id"], tid)
        self.assertEqual(row["title"], "Buy milk")
        self.assertEqual(row["is_done"], 0)
        self.assertIsNotNone(row["created_at"])

    def test_update_title_and_done(self):
        tid = insert_task(self.conn, "Initial title")  

        count = update_task(self.conn, tid, title="Updated title")
        self.assertEqual(count, 1)
        row = self.fetch_all()[0]
        self.assertEqual(row["title"], "Updated title")
        self.assertEqual(row["is_done"], 0)

        count = update_task(self.conn, tid, done=1)
        self.assertEqual(count, 1)
        row = self.fetch_all()[0]
        self.assertEqual(row["is_done"], 1)

        count = update_task(self.conn, tid, title="Final title", done=0)
        self.assertEqual(count, 1)
        row = self.fetch_all()[0]
        self.assertEqual(row["title"], "Final title")
        self.assertEqual(row["is_done"], 0)

    def test_update_with_no_fields_returns_zero(self):
        tid = insert_task(self.conn, "No-op")
        count = update_task(self.conn, tid)  
        self.assertEqual(count, 0)
        row = self.fetch_all()[0]
        self.assertEqual(row["title"], "No-op")
        self.assertEqual(row["is_done"], 0)

    def test_delete_existing_and_nonexistent(self):
        tid = insert_task(self.conn, "To delete")
        count = delete_task(self.conn, tid)
        self.assertEqual(count, 1)
        self.assertEqual(self.fetch_all(), [])

        count = delete_task(self.conn, tid)
        self.assertEqual(count, 0)

if __name__ == "__main__":
    unittest.main()