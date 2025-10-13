"""
Library Service Module - Business Logic Functions
Contains all the core business logic for the Library Management System
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from database import (
    get_book_by_id, get_book_by_isbn, get_patron_borrow_count,
    insert_book, insert_borrow_record, update_book_availability,
    update_borrow_record_return_date, get_all_books,get_patron_borrowed_books, get_patron_borrowing_history
)

def add_book_to_catalog(title: str, author: str, isbn: str, total_copies: int) -> Tuple[bool, str]:
    """
    Add a new book to the catalog.
    Implements R1: Book Catalog Management
    
    Args:
        title: Book title (max 200 chars)
        author: Book author (max 100 chars)
        isbn: 13-digit ISBN
        total_copies: Number of copies (positive integer)
        
    Returns:
        tuple: (success: bool, message: str)
    """
    # Input validation
    if not title or not title.strip():
        return False, "Title is required."
    
    if len(title.strip()) > 200:
        return False, "Title must be less than 200 characters."
    
    if not author or not author.strip():
        return False, "Author is required."
    
    if len(author.strip()) > 100:
        return False, "Author must be less than 100 characters."
    
    if len(isbn) != 13 or not isbn.isdigit():
        return False, "ISBN must be exactly 13 digits."
    
    if not isinstance(total_copies, int) or total_copies <= 0:
        return False, "Total copies must be a positive integer."
    
    # Check for duplicate ISBN
    existing = get_book_by_isbn(isbn)
    if existing:
        return False, "A book with this ISBN already exists."
    
    # Insert new book
    success = insert_book(title.strip(), author.strip(), isbn, total_copies, total_copies)
    if success:
        return True, f'Book "{title.strip()}" has been successfully added to the catalog.'
    else:
        return False, "Database error occurred while adding the book."

def borrow_book_by_patron(patron_id: str, book_id: int) -> Tuple[bool, str]:
    """
    Allow a patron to borrow a book.
    Implements R3 as per requirements  
    
    Args:
        patron_id: 6-digit library card ID
        book_id: ID of the book to borrow
        
    Returns:
        tuple: (success: bool, message: str)
    """
    # Validate patron ID
    if not patron_id or not patron_id.isdigit() or len(patron_id) != 6:
        return False, "Invalid patron ID. Must be exactly 6 digits."
    
    # Check if book exists and is available
    book = get_book_by_id(book_id)
    if not book:
        return False, "Book not found."
    
    if book['available_copies'] <= 0:
        return False, "This book is currently not available."
    
    # Check patron's current borrowed books count
    current_borrowed = get_patron_borrow_count(patron_id)
    
    if current_borrowed >= 5:
        return False, "You have reached the maximum borrowing limit of 5 books."
    
    # Create borrow record
    borrow_date = datetime.now()
    due_date = borrow_date + timedelta(days=14)
    
    # Insert borrow record and update availability
    borrow_success = insert_borrow_record(patron_id, book_id, borrow_date, due_date)
    if not borrow_success:
        return False, "Database error occurred while creating borrow record."
    
    availability_success = update_book_availability(book_id, -1)
    if not availability_success:
        return False, "Database error occurred while updating book availability."
    
    return True, f'Successfully borrowed "{book["title"]}". Due date: {due_date.strftime("%Y-%m-%d")}.'

def return_book_by_patron(patron_id: str, book_id: int) -> Tuple[bool, str]:
    """
    Process book return by a patron.
    """
    if not patron_id or not patron_id.isdigit() or len(patron_id) != 6:
        return False, "Invalid patron ID. Must be exactly 6 digits."
    
    # Check if book exists
    book = get_book_by_id(book_id)
    if not book:
        return False, "Book not found."
    
    borrowed_books = get_patron_borrowed_books(patron_id)
    
    book_match_flag = False
    for borrowed_book in borrowed_books:
        if book["id"] == borrowed_book["book_id"]:
            book_match_flag = True
    if not book_match_flag:
        return False, "Book not borrowed by patron"
    
    late_fee = calculate_late_fee_for_book(patron_id, book_id)
    if "success" not in late_fee["status"].lower():
        return False,f'Late fee calculation failed: {late_fee["status"].lower()}'
    
    return_date = datetime.now()
    
    return_date_success = update_borrow_record_return_date(patron_id, book_id, return_date)
    if not return_date_success :
        return False, "Database error occured while updating book return date"
    
    availability_success = update_book_availability(book_id, 1)
    if not availability_success:
        return False, "Database error occurred while updating book availability."
    

    
    return True, f'Successfully returned "{book["title"]}". Late fees owed: {late_fee["fee_amount"]}'

def calculate_late_fee_for_book(patron_id: str, book_id: int) -> Dict:
    """
    Calculate late fees for a specific book.
    """
    late_fee = {
        'fee_amount': 0.00,
        'days_overdue': 0,
        'status': ''
    }
    if not patron_id or not patron_id.isdigit() or len(patron_id) != 6:
        late_fee["status"] = "Invalid patron ID. Must be exactly 6 digits."
        return late_fee
    
    # Check if book exists
    book = get_book_by_id(book_id)
    
    if not book:
        late_fee["status"] = "Book not found."
        return late_fee 
    
    borrowed_books = get_patron_borrowed_books(patron_id)
    
    for borrowed_book in borrowed_books:
        if book["id"] == borrowed_book["book_id"]:
            break
    else :    
        late_fee["status"] = "Book not borrowed by patron."
        return late_fee
    
    if datetime.now() > borrowed_book['due_date']:
        days_overdue = datetime.now() - borrowed_book['due_date']
        if days_overdue.days <= 7 :
            fees = days_overdue.days * 0.50
        elif days_overdue.days < 19 and days_overdue.days > 7:
            fees = 3.50 + (days_overdue.days - 7)
        elif  days_overdue.days >= 19 :
            fees = 15.00
        
        late_fee["days_overdue"] = days_overdue.days
        late_fee["fee_amount"] = fees
    
    late_fee["status"] = "Successfully calculated overdue fees"
    return late_fee
        
    

def search_books_in_catalog(search_term: str, search_type: str) -> List[Dict]:
    """
    Search for books in the catalog.
    """
    results = []
    
    if search_type == "isbn":
        results.append(get_book_by_isbn(search_term))
    elif search_type == "title":
        books = get_all_books()
        for book in books:
            if search_term in book['title']:
                results.append(book)
    elif search_type == "author":
        books = get_all_books()
        for book in books:
            if search_term in book['author']:
                results.append(book)
    return results

def get_patron_status_report(patron_id: str) -> Dict:
    """
    Get status report for a patron.
    """
    
    if not patron_id or not patron_id.isdigit() or len(patron_id) != 6:
        #returning empty report to avoid cofusion with new account with no activity
        patron_report = {}
        return patron_report
    
    patron_report = {
        'borrowed'  : [],
        'fees_owed' : 0.00,
        'books_out' : 0,
        'history' : []
    }
    
    borrowed_books = get_patron_borrowed_books(patron_id)
    
    patron_report["borrowed"] = borrowed_books
    patron_report["books_out"] = len(borrowed_books)
    for book in borrowed_books:
        patron_report["fees_owed"] = patron_report["fees_owed"] + calculate_late_fee_for_book(patron_id, book["book_id"])['fee_amount']
    
    patron_report["history"] = get_patron_borrowing_history(patron_id)
    
    return patron_report
