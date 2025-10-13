import library_service
from flask import Flask
from routes import register_blueprints
from database import init_database, add_sample_data, get_book_by_id
from tests import  test_R5, test_R1
import os
import pytest



if __name__ == '__main__':
    ##os.remove("./library.db")
    #init_database()
    #add_sample_data()
    print("R1 tests start")
    #R1_tests.test_add_book_invalid_author_too_long()
    #R1_tests.test_add_book_invalid_isbn_characters()
    #R1_tests.test_add_book_invalid_isbn_too_short()
    #R1_tests.test_add_book_negative_copies()
    test_R1.test_add_book_valid_input()
    print("PASS")

    
    
    print("R3 tests start")
    #R3_tests.test_borrow_book_valid_input()
    #R3_tests.test_borrow_book_unavailable()
    #R3_tests.test_borrow_book_above_borrow_limit()
    print("PASS")
    
    #app = create_app()
    
    #app.secret_key = "super secret key"
    
    #register_blueprints(app)
    #R2_tests.test_catalog_valid_new_data(app)
    #R2_tests.test_catalog_valid_avail_0_1()
    #R2_tests.test_catalog_valid_avail_1_3()
    #R2_tests.test_catalog_valid_new_data()
    
    print(get_book_by_id(1).keys())
