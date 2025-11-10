"""
Unit Tests for R2: Book Catalog Display
Tests the functionality of displaying all books in the catalog with proper formatting
"""

import os
from datetime import datetime, timedelta
from database import init_database, get_all_books, insert_book, get_book_by_isbn, add_sample_data
from services.library_service import search_books_in_catalog





def test_display_all_books_with_complete_information():
    """
    Test that all books are retrieved with complete fields
    """    
    os.remove("./library.db")
    init_database()
    # Add test books
    insert_book('Test', 'john', '00010200300', 5, 3)
    insert_book('test2', 'jane', '00010200302', 2, 0)        
    # Get all books
    books = get_all_books()
    assert len(books) == 2, f"Expected 2 books in catalog, got {len(books)}"
    
    required_fields = ['id', 'title', 'author', 'isbn', 'available_copies', 'total_copies']
        
    for book in books:
        for field in required_fields:
            assert field in book
    add_sample_data()


def test_display_shows_available_copies_correctly():
    """
    Test that the display correctly shows available copies vs total copies
    """
    
        # Add test books with different availability
    insert_book('Available Book', 'John Doe', '1234567890123', 3, 2)
    insert_book('Unavailable Book', 'Jane Smith', '9876543210987', 1, 0)
        
    books = get_all_books()
        
    # Find the available book
    for book in books :
        if book['title'] == 'Available Book':
            available_book = book
        if book['title'] == 'Unavailable Book':
            unavailable_book = book

    assert available_book is not None
    assert available_book['available_copies'] == 2
    assert available_book['total_copies'] == 3
    assert available_book['available_copies'] > 0
    
    # Find the unavailable book
    assert unavailable_book is not None
    assert unavailable_book['available_copies'] == 0
    assert unavailable_book['total_copies'] == 1
        


def test_display_handles_empty_catalog():
    """
    Test that the display handles an empty catalog
    """
    os.remove("./library.db")
    init_database()

    books = get_all_books()
        
    assert isinstance(books, list)
    assert len(books) == 0
    add_sample_data()
        

def  test_display_search_book():
    """Test search books with full isbn"""
    os.remove("./library.db")
    init_database()
    add_sample_data()
    search_dict = search_books_in_catalog("9780743273565","isbn")
    assert 'F. Scott Fitzgerald' in search_dict[0]['author']
    assert 'The Great Gatsby' in search_dict[0]['title']

