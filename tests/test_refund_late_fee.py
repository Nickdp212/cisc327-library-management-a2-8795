from services.library_service import refund_late_fee_payment
from unittest.mock import Mock
import time
from services.payment_service import PaymentGateway

def test_successful_refund():
    mock_pg=Mock(spec=PaymentGateway)
    
    transaction_id= f"txn_800000_{int(time.time())}"
    refund_id = f"refund_{transaction_id}_{int(time.time())}"
    amount = 15.0
    mock_pg.refund_payment.return_value = True, f"Refund of ${amount:.2f} processed successfully. Refund ID: {refund_id}"
    
    status, message = refund_late_fee_payment(transaction_id,amount,mock_pg)
    
    mock_pg.refund_payment.assert_called_once_with(transaction_id,amount)
    assert status == True
    assert message == f"Refund of $15.00 processed successfully. Refund ID: {refund_id}"

def test_invalid_transaction():
    mock_pg=Mock(spec=PaymentGateway)
    
    transaction_id= f"abcd"
    amount = 15.0    
    status, message = refund_late_fee_payment(transaction_id,amount,mock_pg)
    
    assert status == False
    assert message == "Invalid transaction ID."
    mock_pg.refund_payment.assert_not_called()

def test_invalid_large_refund():
    mock_pg=Mock(spec=PaymentGateway)
    
    transaction_id= f"txn_800000_{int(time.time())}"
    refund_id = f"refund_{transaction_id}_{int(time.time())}"
    amount = 15.1
    
    status, message = refund_late_fee_payment(transaction_id,amount,mock_pg)
    
    mock_pg.refund_payment.assert_not_called()
    assert status == False
    assert message == f"Refund amount exceeds maximum late fee."
    
def test_invalid_negative_refund():
    mock_pg=Mock(spec=PaymentGateway)
    
    transaction_id= f"txn_800000_{int(time.time())}"
    refund_id = f"refund_{transaction_id}_{int(time.time())}"
    amount = -0.5
    
    status, message = refund_late_fee_payment(transaction_id,amount,mock_pg)
    
    mock_pg.refund_payment.assert_not_called()
    assert status == False
    assert message == f"Refund amount must be greater than 0."

def test_invalid_0_refund():
    mock_pg=Mock(spec=PaymentGateway)
    
    transaction_id= f"txn_800000_{int(time.time())}"
    refund_id = f"refund_{transaction_id}_{int(time.time())}"
    amount = 0.0
    
    status, message = refund_late_fee_payment(transaction_id,amount,mock_pg)
    
    mock_pg.refund_payment.assert_not_called()
    assert status == False
    assert message == f"Refund amount must be greater than 0."
#extra    
def test_error_handling():
    mock_pg=Mock(spec=PaymentGateway)
    
    transaction_id= f"txn_800000_{int(time.time())}"
    refund_id = f"refund_{transaction_id}_{int(time.time())}"
    amount = 15.0
    mock_pg.refund_payment.return_value = Exception
    
    status, message = refund_late_fee_payment(transaction_id,amount,mock_pg)
    
    mock_pg.refund_payment.assert_called_once_with(transaction_id,amount)
    assert status == False
    assert message == f"Refund processing error: cannot unpack non-iterable type object"