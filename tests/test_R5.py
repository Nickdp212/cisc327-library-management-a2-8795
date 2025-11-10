from services.library_service import calculate_late_fee_for_book, borrow_book_by_patron
from database import insert_borrow_record, init_database, add_sample_data
import os
from datetime import datetime, timedelta
import pytest


def test_fee_calculation_no_fee(mocker):
    mocker.patch('services.library_service.get_book_by_id', return_value={
        'id': 1,
        'title': 'Test Book',
        'available_copies': 2
    })

    borrow_date = datetime.now()
    due_date = borrow_date + timedelta(days=14)  # Not overdue
    mocker.patch('services.library_service.get_patron_borrowed_books', return_value=[{
        'book_id': 1,
        'borrow_date': borrow_date,
        'due_date': due_date,
        'is_overdue': False
    }])
    
    fee_dict = calculate_late_fee_for_book("500000", 1)
    
    assert fee_dict['fee_amount'] == 0.00
    assert fee_dict['days_overdue'] == 0
    assert "success" in fee_dict['status'].lower()

def test_fee_calculation_fee(mocker):
   #inserting borrowing record

    mocker.patch('services.library_service.get_book_by_id', return_value={
        'id': 1,
        'title': 'Test Book',
        'available_copies': 2
    })

    borrow_date = datetime.now()
    due_date = borrow_date - timedelta(days=7)  # 7 days overdue
    mocker.patch('services.library_service.get_patron_borrowed_books', return_value=[{
        'book_id': 1,
        'borrow_date': borrow_date,
        'due_date': due_date,
        'is_overdue': False
    }])
    """Test fee calculation with valid inputs that result in a 3.50$ fee"""
    fee_dict = calculate_late_fee_for_book("050000", 1)
    assert "success" in fee_dict['status'].lower()

    assert 3.50 == fee_dict['fee_amount']
    assert 7 == fee_dict['days_overdue']

def test_fee_calculation_max_fee(mocker):
    mocker.patch('services.library_service.get_book_by_id', return_value={
        'id': 1,
        'title': 'Test Book',
        'available_copies': 2
    })

    borrow_date = datetime.now()
    due_date = borrow_date - timedelta(days=25) # 25 days overdue
    mocker.patch('services.library_service.get_patron_borrowed_books', return_value=[{
        'book_id': 1,
        'borrow_date': borrow_date,
        'due_date': due_date,
        'is_overdue': False
    }])
    """Test fee calculation with valid inputs that result in a 15$ fee"""
    fee_dict = calculate_late_fee_for_book("005000", 1)
    
    assert 15.0 == fee_dict['fee_amount']
    assert 25 == fee_dict['days_overdue']
    assert "success" in fee_dict['status'].lower()

def  test_fee_calculation_unborrowed_book(mocker):
    mocker.patch('services.library_service.get_book_by_id', return_value={
        'id': 1,
        'title': 'Test Book',
        'available_copies': 2
    })

    borrow_date = datetime.now()
    due_date = borrow_date + timedelta(days=14)  
    mocker.patch('services.library_service.get_patron_borrowed_books', return_value=[{
        'book_id': 2, #not borrowed by patron
        'borrow_date': borrow_date,
        'due_date': due_date,
        'is_overdue': False
    }])
    
    """Test fee calculation with a book that is not borrowed"""
    fee_dict = calculate_late_fee_for_book("000500", 1)
    
    assert 0.00 == fee_dict['fee_amount']
    assert 0 == fee_dict['days_overdue']
    assert "not borrowed" in fee_dict['status'].lower()
    
#New
def test_fee_calculation_medium_fee(mocker):

    mocker.patch('services.library_service.get_book_by_id', return_value={
        'id': 1,
        'title': 'Test Book',
        'available_copies': 2
    })

    borrow_date = datetime.now()
    due_date = borrow_date - timedelta(days=10)  # 7 days overdue
    mocker.patch('services.library_service.get_patron_borrowed_books', return_value=[{
        'book_id': 1,
        'borrow_date': borrow_date,
        'due_date': due_date,
        'is_overdue': False
    }])
    """Test fee calculation with valid inputs that result in a 6.50$ fee"""
    fee_dict = calculate_late_fee_for_book("050000", 1)
    assert "success" in fee_dict['status'].lower()

    assert 6.50 == fee_dict['fee_amount']
    assert 10 == fee_dict['days_overdue']

def test_fee_calculation_no_book(mocker):
    mocker.patch('services.library_service.get_book_by_id', return_value={})
    
    """Test fee calculation with a non-existant book"""
    
    fee_dict = calculate_late_fee_for_book("050000", 1)
    assert 0.00 == fee_dict['fee_amount']
    assert 0 == fee_dict['days_overdue']
    assert "not found" in fee_dict['status'].lower()

def test_fee_calculation_invalid_id(mocker):
    
    """Test fee calculation with a invalid patron id"""
    
    fee_dict = calculate_late_fee_for_book("abcdefg", 1)
    assert 0.00 == fee_dict['fee_amount']
    assert 0 == fee_dict['days_overdue']
    assert " 6 digits." in fee_dict['status'].lower()