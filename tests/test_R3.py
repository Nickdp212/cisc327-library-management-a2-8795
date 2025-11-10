import pytest
from services.library_service import borrow_book_by_patron, add_book_to_catalog


def  test_borrow_book_valid_input():

    """Test borrowing with valid inputs"""
    success, message =  borrow_book_by_patron("123456", 1)
    
    assert success == True
    assert "successfully borrowed" in message.lower()
    
def test_borrow_book_unavailable():

    """Test borrowing with unvailable book"""
    success, message =  borrow_book_by_patron("123456", 3)
    
    assert success == False
    assert "not available" in message.lower()
    
def test_borrow_book_invalid_patron_id():

    
    """Test borrowing with Invalid patron id"""

    success, message =  borrow_book_by_patron("12a456", 1)
    
    assert success == False
    assert "6 digits" in message.lower()
    

def test_borrow_book_above_borrow_limit():
    #adding test book as there are insufficient sample books to test this feature
    add_book_to_catalog("Test Book", "Test Author", "1234567890123", 5)
    borrow_book_by_patron("123456", 4 )
    borrow_book_by_patron("123456", 4 )
    borrow_book_by_patron("123456", 4 )
    borrow_book_by_patron("123456", 4 )
    borrow_book_by_patron("123456", 4 )
    
    """Test borrowing above borrow limit"""
    success, message =  borrow_book_by_patron("123456", 2)
    assert success == False
    assert "borrowing limit" in message.lower()  
