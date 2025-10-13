import pytest
from library_service import return_book_by_patron, borrow_book_by_patron
from database import insert_borrow_record
from datetime import datetime, timedelta

def  test_return_book_valid_input():
    #borrowing book 
    insert_borrow_record("400000", 2, datetime.now(), datetime.now() + timedelta(days=14) )
    """Test borrowing with valid inputs"""
    success, message =  return_book_by_patron("400000", 2)
    
    #assert success == True
    assert "successfully returned" in message.lower()

def  test_return_book_unborrowed_book():
    #borrowing book 
    borrow_book_by_patron("040000", 1)
    
    """Test borrowing with valid inputs"""
    success, message =  return_book_by_patron("040000", 2)
    
    assert success == False
    assert "book not borrowed by patron" in message.lower()

def  test_return_book_non_existant_book():
    #borrowing book 
    borrow_book_by_patron("004000", 1)
    
    """Test borrowing with valid inputs"""
    success, message =  return_book_by_patron("004000", 55)
    
    assert success == False
    assert "book not found" in message.lower()


def  test_return_book_invalid_patron_id():

    """Test borrowing with valid inputs"""
    success, message =  return_book_by_patron("12abcd", 1)
    
    assert success == False
    assert "invalid patron id" in message.lower()
