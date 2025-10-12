import unittest
from accounts import Account

class TestAccount(unittest.TestCase):
    def setUp(self):
        self.account = Account('user123', 1000.0)

    def test_initial_balance(self):
        self.assertEqual(self.account.balance, 1000.0)

    def test_deposit(self):
        self.account.deposit(500.0)
        self.assertEqual(self.account.balance, 1500.0)

    def test_withdraw_success(self):
        success = self.account.withdraw(200.0)
        self.assertTrue(success)
        self.assertEqual(self.account.balance, 800.0)

    def test_withdraw_insufficient_funds(self):
        success = self.account.withdraw(2000.0)
        self.assertFalse(success)
        self.assertEqual(self.account.balance, 1000.0)

    def test_buy_shares_success(self):
        success = self.account.buy_shares('AAPL', 5)
        self.assertTrue(success)
        self.assertIn('AAPL', self.account.get_holdings())
        self.assertEqual(self.account.get_holdings()['AAPL'], 5)

    def test_buy_shares_insufficient_funds(self):
        success = self.account.buy_shares('AAPL', 10)
        self.assertFalse(success)

    def test_sell_shares_success(self):
        self.account.buy_shares('AAPL', 5)
        success = self.account.sell_shares('AAPL', 3)
        self.assertTrue(success)
        self.assertEqual(self.account.get_holdings()['AAPL'], 2)

    def test_sell_shares_not_enough(self):
        self.account.buy_shares('AAPL', 2)
        success = self.account.sell_shares('AAPL', 3)
        self.assertFalse(success)

    def test_calculate_portfolio_value(self):
        self.account.deposit(500.0)
        self.account.buy_shares('AAPL', 5)
        self.assertAlmostEqual(self.account.calculate_portfolio_value(), 1500.0 + 5 * 150.0)

    def test_profit_loss(self):
        self.assertEqual(self.account.get_profit_loss(), 0.0)
        self.account.deposit(500.0)
        self.account.buy_shares('AAPL', 5)
        self.assertAlmostEqual(self.account.get_profit_loss(), (500.0 + 5 * 150.0) - 1000.0)

if __name__ == '__main__':
    unittest.main()