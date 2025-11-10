from services.library_service import  search_books_in_catalog
import pytest

def  test_search_book_isbn():
    
    """Test search books with full isbn"""
    search_dict = search_books_in_catalog("9780743273565","isbn")
    assert 'F. Scott Fitzgerald' in search_dict[0]['author']
    assert 'The Great Gatsby' in search_dict[0]['title']
    
def  test_search_partial_title():
    """Test search books with partial title"""
    search_dict = search_books_in_catalog("The Gre","title")
    assert 'F. Scott Fitzgerald' in search_dict[0]['author']
    assert 'The Great Gatsby' in search_dict[0]['title']
    
def  test_search_null_book():
    """Test search book that doesnt exist"""
    search_dict = search_books_in_catalog("abcdefg","title")
    assert  not  search_dict
    
def test_search_multiple_authors():
    """Test search book with multiple authors fitting"""
    search_dict = search_books_in_catalog("g","author")
    assert 'F. Scott Fitzgerald'  in search_dict[1]['author']
    assert 'The Great Gatsby'  in search_dict[1]['title']
    assert 'George Orwell'  in search_dict[0]['author']
    assert '1984'  in search_dict[0]['title']
    assert len(search_dict) == 2

