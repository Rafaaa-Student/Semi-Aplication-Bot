import sqlite3
import os

# Path ke database
DB_DIR = os.path.dirname(__file__)
DB_FILE = os.path.join(DB_DIR, 'books.db')

def get_db_connection():
    """Create and return database connection"""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database with books table and indexes"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create books table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            judul TEXT NOT NULL,
            harga TEXT,
            deskripsi TEXT,
            url TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create indexes for faster search
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_judul ON books(judul)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_deskripsi ON books(deskripsi)')
    
    conn.commit()
    conn.close()

def add_book(judul, harga, deskripsi, url):
    """Add a new book to database"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO books (judul, harga, deskripsi, url)
        VALUES (?, ?, ?, ?)
    ''', (judul, harga, deskripsi, url))
    conn.commit()
    book_id = cursor.lastrowid
    conn.close()
    return book_id

def get_books(limit=None, offset=0):
    """Get books from database with optional limit and offset"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if limit:
        cursor.execute('SELECT * FROM books ORDER BY id DESC LIMIT ? OFFSET ?', (limit, offset))
    else:
        cursor.execute('SELECT * FROM books ORDER BY id DESC')
    
    books = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return books

def search_books(keyword):
    """Search books by judul or deskripsi (case-insensitive)"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    search_term = f'%{keyword}%'
    cursor.execute('''
        SELECT * FROM books 
        WHERE LOWER(judul) LIKE LOWER(?) 
           OR LOWER(deskripsi) LIKE LOWER(?)
        ORDER BY id DESC
    ''', (search_term, search_term))
    
    results = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return results

def get_book_count():
    """Get total number of books in database"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) as count FROM books')
    count = cursor.fetchone()['count']
    conn.close()
    return count

def book_exists(judul):
    """Check if a book with given judul already exists"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM books WHERE judul = ?', (judul,))
    result = cursor.fetchone()
    conn.close()
    return result is not None

def get_random_book():
    """Get a random book from database"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM books ORDER BY RANDOM() LIMIT 1')
    book = cursor.fetchone()
    conn.close()
    return dict(book) if book else None

# Initialize database on import
if __name__ != '__main__':
    init_db()
