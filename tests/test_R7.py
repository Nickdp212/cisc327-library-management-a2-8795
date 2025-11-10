from services.library_service import  get_patron_status_report, borrow_book_by_patron
from database import insert_borrow_record
from datetime import datetime ,timedelta
import pytest

def  test_patron_valid_id():
    """Test get patron with no data"""
    patron_dict = get_patron_status_report("700000")
    assert not patron_dict['borrowed']
    assert 0.00 == patron_dict['fees_owed']
    assert 0 == patron_dict['books_out']
    assert not patron_dict['history']
    
    
def  test_patron_valid_fees():
    due_date = datetime.now()- timedelta(days=7)
    insert_borrow_record("070000", 1, datetime.now(), due_date )
    """Test patron status with valid inputs that result in a 3.50$ fee"""
    patron_dict = get_patron_status_report("070000")
    assert 1 == patron_dict['borrowed'][0]['book_id']
    assert 3.50 == patron_dict['fees_owed']
    assert 1 == patron_dict['books_out']
    assert  due_date== patron_dict['borrowed'][0]['due_date']

def  test_patron_multiple_fees():
    insert_borrow_record("007000", 1, datetime.now(), datetime.now()- timedelta(days=30))
    insert_borrow_record("007000", 2, datetime.now(), datetime.now()- timedelta(days=30))

    """Test patron status with valid inputs that result in a 30$ fee from multiple books"""
    patron_dict = get_patron_status_report("007000")
    assert 1  == patron_dict['borrowed'][0]['book_id']
    assert 2 == patron_dict['borrowed'][1]['book_id']
    assert 30.0 == patron_dict['fees_owed']
    assert 2 == patron_dict['books_out']

def test_patron_invalid_id():
    """Test patron status with invalid patron id"""
    patron_dict = get_patron_status_report("0000ab")
    assert not patron_dict
