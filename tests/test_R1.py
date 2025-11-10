import pytest
from services.library_service import (
    add_book_to_catalog
)
import database
import os

def test_add_book_valid_input():
    """Test adding a book with valid input."""
    os.remove("./library.db")

    database.init_database()
    database.add_sample_data()
    success, message = add_book_to_catalog("Test Book", "Test Author", "1234567890123", 5)
    
    assert success == True
    assert "successfully added" in message.lower()
    

def test_add_book_invalid_isbn_too_short():
    """Test adding a book with ISBN too short."""
    success, message = add_book_to_catalog("Test Book", "Test Author", "123456789", 5)
    
    assert success == False
    assert "13 digits" in message

def test_add_book_invalid_isbn_characters():
    """Test adding non-digits to ISBN"""
    success, message = add_book_to_catalog("Test Book", "Test Author", "123456789abcd", 5)
    
    assert success == False
    assert "13 digits" in message.lower()



def test_add_book_negative_copies():
    """Test adding a book with negative copies."""
    success, message = add_book_to_catalog("Test Book", "Test Author", "1234567890123", -1)
    
    assert success == False
    assert "positive integer" in message.lower()

def test_add_book_invalid_author_too_long():
    """Test adding a book with a 116 character author."""
    success, message = add_book_to_catalog("Test Book", "ytxsRrNndveZUntHXmdpaqfvwApVQpgMHKdDbsRpSqYgAwhVKhUXJsYkVCgtkXDKCpJUSyGMbxnWRNFnqMEvvyGzmwwGaXGVJyNMextra_characters", "1234567890123", 5)
    
    assert success == False
    assert "100 characters" in message.lower()
    
#new
def test_add_book_no_title():
    """Test adding a book with no title"""
    success, message = add_book_to_catalog("", "Test Author", "123456789", 5)
    
    assert success == False
    assert "Title is required." in message

def test_add_book_no_author():
    """Test adding a book with no author"""
    success, message = add_book_to_catalog("test", "", "123456789", 5)
    
    assert success == False
    assert "Author is required." in message

def test_add_book_invalid_title_too_long():
    """Test adding a book with a 232 character title."""
    success, message = add_book_to_catalog("ytxsRrNndveZUntHXmdpaqfvwApVQpgMHKdDbsRpSqYgAwhVKhUXJsYkVCgtkXDKCpJUSyGMbxnWRNFnqMEvvyGzmwwGaXGVJyNMextra_charactersytxsRrNndveZUntHXmdpaqfvwApVQpgMHKdDbsRpSqYgAwhVKhUXJsYkVCgtkXDKCpJUSyGMbxnWRNFnqMEvvyGzmwwGaXGVJyNMextra_characters", "Test Author", "1234567890123", 5)
    
    assert success == False
    assert "200 characters" in message.lower()

def test_add_book_existing_isbn(mocker):
    """Test adding a book that collides with another isbn"""
    mocker.patch('services.library_service.get_book_by_isbn', return_value={
        'title' : "test_book"
        
    })
    success, message = add_book_to_catalog("Test Book", "Test Author", "1234567890123", 5)
    
    assert success == False
    assert "already exists" in message.lower()
    

    