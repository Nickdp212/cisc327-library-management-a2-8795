from services.library_service import pay_late_fees
from unittest.mock import Mock
import time
from services.payment_service import PaymentGateway


def test_successful_payment(mocker):
    mocker.patch('services.library_service.calculate_late_fee_for_book', return_value={
        'fee_amount': 3.00,
        'days_overdue': 6,
        'status': 'Successfully calculated overdue fees'
    })
    mocker.patch('services.library_service.get_book_by_id', return_value={
        'title' : "test_book"
    })
    
    mock_pg=Mock(spec=PaymentGateway)
    
    
    
    transaction_id= f"txn_800000_{int(time.time())}"
    
    mock_pg.process_payment.return_value = True, transaction_id,"Payment of $3.00 processed successfully" 
    status, message, t_id = pay_late_fees("800000",1,mock_pg)
    
    mock_pg.process_payment.assert_called_once_with(patron_id='800000', amount=3.0, description="Late fees for 'test_book'")
    assert status == True
    assert message == "Payment successful! Payment of $3.00 processed successfully"
    assert t_id == transaction_id
    

def test_declined_payment(mocker):
    mocker.patch('services.library_service.calculate_late_fee_for_book', return_value={
        'fee_amount': 1001,
        'days_overdue': 6,
        'status': 'Successfully calculated overdue fees'
    })
    mocker.patch('services.library_service.get_book_by_id', return_value={
        'title' : "test_book"
    })
    
    mock_pg=Mock(spec=PaymentGateway)
    
    mock_pg.process_payment.return_value = False,None, "Payment declined: amount exceeds limit" 
    status, message, t_id = pay_late_fees("080000",1,mock_pg)
    
    mock_pg.process_payment.assert_called_once_with(patron_id='080000', amount=1001.0, description="Late fees for 'test_book'")
    assert status == False
    assert message == "Payment failed: Payment declined: amount exceeds limit"
    assert t_id == None
    
def test_invalid_patron_id(mocker):
    mock_pg=Mock(spec=PaymentGateway)
    
    status, message, t_id = pay_late_fees("ABCDEF",1,mock_pg)
    
    mock_pg.process_payment.assert_not_called()
    assert status == False
    assert message == "Invalid patron ID. Must be exactly 6 digits."
    assert t_id == None
    
def test_no_fee(mocker):
    mocker.patch('services.library_service.calculate_late_fee_for_book', return_value={
        'fee_amount': 0,
        'days_overdue': 0,
        'status': 'Successfully calculated overdue fees'
    })
    mocker.patch('services.library_service.get_book_by_id', return_value={
        'title' : "test_book"
    })
    
    mock_pg=Mock(spec=PaymentGateway)
    
    mock_pg.process_payment.return_value = False,None, "" 
    status, message, t_id = pay_late_fees("008000",1,mock_pg)
    
    mock_pg.process_payment.assert_not_called()
    assert status == False
    assert message == "No late fees to pay for this book."
    assert t_id == None
    
def test_network_error(mocker):
    mocker.patch('services.library_service.calculate_late_fee_for_book', return_value={
        'fee_amount': 3.00,
        'days_overdue': 6,
        'status': 'Successfully calculated overdue fees'
    })
    mocker.patch('services.library_service.get_book_by_id', return_value={
        'title' : "test_book"
    })
    
    mock_pg=Mock(spec=PaymentGateway)
        
    transaction_id= f"txn_800000_{int(time.time())}"
    
    mock_pg.process_payment.side_effect = Exception 
    status, message, t_id = pay_late_fees("800000",1,mock_pg)
    
    mock_pg.process_payment.assert_called_once_with(patron_id='800000', amount=3.0, description="Late fees for 'test_book'")
    assert status == False
    assert message == "Payment processing error: "
    assert t_id == None