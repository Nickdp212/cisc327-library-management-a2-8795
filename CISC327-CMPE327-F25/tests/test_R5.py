from library_service import calculate_late_fee_for_book, borrow_book_by_patron
from database import insert_borrow_record, init_database, add_sample_data
import os
from datetime import datetime, timedelta
import pytest

def test_fee_calculation_no_fee():
   #borrowing book 
    insert_borrow_record("500000", 1, datetime.now(), datetime.now() + timedelta(days=14) )
    
    """Test fee calculation with valid inputs"""
    fee_dict = calculate_late_fee_for_book("500000", 1)
    
    assert 0.00 == fee_dict['fee_amount']
    assert 0 == fee_dict['days_overdue']
    assert "success" in fee_dict['status'].lower()


def test_fee_calculation_fee():
   #inserting borrowing record

    insert_borrow_record("050000", 1, datetime.now(), datetime.now() - timedelta(days=7) )
    
    """Test fee calculation with valid inputs that result in a 3.50$ fee"""
    fee_dict = calculate_late_fee_for_book("050000", 1)
    assert "success" in fee_dict['status'].lower()

    assert 3.50 == fee_dict['fee_amount']
    assert 7 == fee_dict['days_overdue']

def test_fee_calculation_max_fee():
   #inserting borrowing record
    insert_borrow_record("005000", 1, datetime.now(), datetime.now()- timedelta(days=25))
    """Test fee calculation with valid inputs that result in a 15$ fee"""
    fee_dict = calculate_late_fee_for_book("005000", 1)
    
    assert 15.0 == fee_dict['fee_amount']
    assert 25 == fee_dict['days_overdue']
    assert "success" in fee_dict['status'].lower()

def  test_fee_calculation_unborrowed_book():
    """Test fee calculation with a book that is not borrowed"""
    fee_dict = calculate_late_fee_for_book("000500", 1)
    
    assert 0.00 == fee_dict['fee_amount']
    assert 0 == fee_dict['days_overdue']
    assert "not borrowed" in fee_dict['status'].lower()