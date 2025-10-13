# Nicolas Poirier 20288795 Group 3


|Feature | Status |Details |
|--- | --- | --- |
|Add Book To Catalog|Partial|there is no check that the isbn is digits, non-digit characters are also accepted|
|Book Catalog Display|Complete||
|Book Borrowing Interface|Partial|Logic allows for patron to check out 6 books since it only checks if the patron has >5 books|
|Book Return Processing|Partial|Missing patron verification, updating available copies and return records, late fee calculation|
|Late Fee Calculation|Partial|Missing late fee calculation in entirety as the return for calculate_late_fee_for_book is commented out|
|Book Search Functionality|Partial| Missing partial match for title/author, exact match for ISBN, and the business function returns an empty list reguardless of input|
|Patron Status Report|Partial|Missing currently borrowed books, Total late fees owed,Number of books borrowed, and borrowing history|

# R1

### test_add_book_valid_input()

Tests default case of adding a book with correct test inputs

### test_add_book_invalid_isbn_too_short()

Test adding a book with a 9 digit isbn

### test_add_book_invalid_isbn_characters()

Tests adding a book with non-digit characters in isbn

### test_add_book_negative_copies()

Tests adding a book with -1 copies

### test_add_book_invalid_author_too_long()

Tests adding a book with 116 character long author

# R3

### test_borrow_book_valid_input()

tests default case for borrowing a book with valid patron id and book

### test_borrow_book_unavailable()

tests borrowing book that has no available copies

### test_borrow_book_invalid_patron_id()

tests borrowing a book with non-digit characters in the patron id

### test_borrow_book_above_borrow_limit()

tests borrowing a book above patron max

# R4

### test_return_book_valid_input()

tests default case of returning books with valid inputs

### test_return_book_unborrowed_book()

tests patron returning book that they had not borrowed

### test_return_book_non_existant_book()

tests patron returning book not in database

### test_return_book_invalid_patron_id()

tests returning book with invalid patron id

# R5

### test_fee_calculation_no_fee()

tests base case of fee calculation with valid inputs that result in no fee

### test_fee_calculation_fee()

tests fee calculation with 7 days of fees  

### test_fee_calculation_max_fee()

tests fee calculation with max fee of 15$ after 25 days

###  test_fee_calculation_unborrowed_book()

tests fee calculation on unborrowed book

# R6

###  test_search_book_isbn()

tests search with full book isbn

###  test_search_partial_title()

tests search with partial title

###  test_search_null_book()

tests search for book not in database

### test_search_multiple_authors()

tests search with returning multiple authors

# R7

###  test_patron_valid_id()

tests patron status on new patron with no records

###  test_patron_valid_fees()

tests patron status with 3.50$ fee

###  test_patron_multiple_fees()

tests patron status with max late fees for multiple books

### test_patron_invalid_id()

tests patron status with invalid patron id with non-digit characters