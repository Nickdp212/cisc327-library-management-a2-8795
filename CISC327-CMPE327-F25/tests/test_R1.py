import pytest
from library_service import (
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


# Add more test methods for each function and edge case. You can keep all your test in a separate folder named `tests`.