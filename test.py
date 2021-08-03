from time import time
import unittest
import importlib

from app import Transaction
from utils import trm
import time

TRM = float(trm(date=time.strftime('%Y-%m-%d'))) 


class TestTransactionMethods(unittest.TestCase):

    def test_deposit_money(self):
        balance = 0
        money = 50000
        transaction = Transaction(user_id='105398891', pin=2090)
        transaction.balance = 0
        result = transaction.deposit_money(money)

        self.assertEqual(result, balance + float(money))

    def test_withdraw_money_in_dollars(self):
        balance = 200000
        money = 50
        transaction = Transaction(user_id='105398891', pin=2090)
        transaction.balance = 200000
        result = transaction.withdraw_money_in_dollars(money)

        self.assertEqual(float(result), balance - float(money * TRM))

    def test_withdraw_money_in_pesos(self):
        balance = 5000
        money = 5000
        transaction = Transaction(user_id='105398891', pin=2090)
        transaction.balance = 5000
        result = transaction.withdraw_money_in_pesos(money)

        self.assertEqual(result, balance - float(money))

if __name__ == '__main__':
    unittest.main()