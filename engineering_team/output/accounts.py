class Account:
    def __init__(self, account_id: str, initial_deposit: float) -> None:
        self.account_id = account_id
        self.balance = initial_deposit
        self.initial_deposit = initial_deposit
        self.holdings = {}
        self.transactions = []
        self.transactions.append({'type': 'deposit', 'amount': initial_deposit})

    def deposit(self, amount: float) -> None:
        self.balance += amount
        self.transactions.append({'type': 'deposit', 'amount': amount})

    def withdraw(self, amount: float) -> bool:
        if amount > self.balance:
            print("Insufficient funds to withdraw.")
            return False
        self.balance -= amount
        self.transactions.append({'type': 'withdraw', 'amount': amount})
        return True

    def buy_shares(self, symbol: str, quantity: int) -> bool:
        price = get_share_price(symbol)
        total_cost = price * quantity
        if total_cost > self.balance:
            print("Insufficient funds to buy shares.")
            return False
        self.balance -= total_cost
        if symbol in self.holdings:
            self.holdings[symbol] += quantity
        else:
            self.holdings[symbol] = quantity
        self.transactions.append({'type': 'buy', 'symbol': symbol, 'quantity': quantity, 'price': price})
        return True

    def sell_shares(self, symbol: str, quantity: int) -> bool:
        if symbol not in self.holdings or self.holdings[symbol] < quantity:
            print("Not enough shares to sell.")
            return False
        price = get_share_price(symbol)
        self.holdings[symbol] -= quantity
        if self.holdings[symbol] == 0:
            del self.holdings[symbol]
        self.balance += price * quantity
        self.transactions.append({'type': 'sell', 'symbol': symbol, 'quantity': quantity, 'price': price})
        return True

    def calculate_portfolio_value(self) -> float:
        total_value = self.balance
        for symbol, quantity in self.holdings.items():
            total_value += quantity * get_share_price(symbol)
        return total_value

    def calculate_profit_loss(self) -> float:
        return self.calculate_portfolio_value() - self.initial_deposit

    def get_holdings(self) -> dict:
        return self.holdings

    def get_profit_loss(self) -> float:
        return self.calculate_profit_loss()

    def list_transactions(self) -> list:
        return self.transactions


def get_share_price(symbol: str) -> float:
    prices = {'AAPL': 150.0, 'TSLA': 700.0, 'GOOGL': 2500.0}
    return prices.get(symbol, 0.0)


def test_account() -> None:
    print('Testing Account Management System')
    account = Account('user123', 1000.0)
    print("Initial Balance:", account.balance)  # Should be 1000.0
    account.deposit(500.0)
    print("Balance after deposit:", account.balance)  # Should be 1500.0
    success = account.withdraw(200.0)
    print("Withdrawal successful:", success)
    print("Balance after withdrawal:", account.balance)  # Should be 1300.0
    success = account.buy_shares('AAPL', 5)
    print("AAPL shares bought:", success)
    print("Holdings after buying AAPL:", account.get_holdings())
    success = account.sell_shares('AAPL', 3)
    print("AAPL shares sold:", success)
    print("Holdings after selling AAPL:", account.get_holdings())
    print("Total Portfolio Value:", account.calculate_portfolio_value())
    print("Profit/Loss:", account.get_profit_loss())

test_account()