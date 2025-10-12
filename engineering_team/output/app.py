from accounts import Account
import gradio as gr

# Global account variable
account = None

def create_account(account_id: str, initial_deposit: float):
    global account
    account = Account(account_id, initial_deposit)
    return f"✅ Account created!\nID: {account_id}\nInitial Deposit: ${initial_deposit}\nCurrent Balance: ${account.balance}"

def deposit_funds(amount: float):
    if account is None:
        return "❌ Please create an account first!"
    account.deposit(amount)
    return f"✅ Deposited: ${amount}\nNew Balance: ${account.balance}"

def withdraw_funds(amount: float):
    if account is None:
        return "❌ Please create an account first!"
    success = account.withdraw(amount)
    if success:
        return f"✅ Withdrew: ${amount}\nNew Balance: ${account.balance}"
    return "❌ Insufficient funds for withdrawal."

def buy_shares(symbol: str, quantity: int):
    if account is None:
        return "❌ Please create an account first!"
    success = account.buy_shares(symbol, quantity)
    if success:
        return f"✅ Bought {quantity} shares of {symbol}\nHoldings: {account.get_holdings()}\nBalance: ${account.balance}"
    return "❌ Insufficient funds to buy shares."

def sell_shares(symbol: str, quantity: int):
    if account is None:
        return "❌ Please create an account first!"
    success = account.sell_shares(symbol, quantity)
    if success:
        return f"✅ Sold {quantity} shares of {symbol}\nHoldings: {account.get_holdings()}\nBalance: ${account.balance}"
    return "❌ Not enough shares to sell."

def portfolio_value():
    if account is None:
        return "❌ Please create an account first!"
    value = account.calculate_portfolio_value()
    return f"📊 Total Portfolio Value: ${value:.2f}"

def profit_loss():
    if account is None:
        return "❌ Please create an account first!"
    profit_loss = account.get_profit_loss()
    status = "📈 Profit" if profit_loss >= 0 else "📉 Loss"
    return f"{status}: ${profit_loss:.2f}"

def transaction_history():
    if account is None:
        return "❌ Please create an account first!"
    transactions = account.list_transactions()
    if not transactions:
        return "No transactions yet."
    
    history = "📋 Transaction History:\n"
    for i, transaction in enumerate(transactions, 1):
        if transaction['type'] == 'deposit':
            history += f"{i}. Deposit: ${transaction['amount']}\n"
        elif transaction['type'] == 'withdraw':
            history += f"{i}. Withdraw: ${transaction['amount']}\n"
        elif transaction['type'] == 'buy':
            history += f"{i}. Buy {transaction['quantity']} {transaction['symbol']} @ ${transaction['price']}\n"
        elif transaction['type'] == 'sell':
            history += f"{i}. Sell {transaction['quantity']} {transaction['symbol']} @ ${transaction['price']}\n"
    
    return history

def get_account_status():
    if account is None:
        return "❌ No account created yet."
    
    status = f"👤 Account ID: {account.account_id}\n"
    status += f"💰 Balance: ${account.balance:.2f}\n"
    status += f"📊 Portfolio Value: ${account.calculate_portfolio_value():.2f}\n"
    status += f"📈 Profit/Loss: ${account.get_profit_loss():.2f}\n"
    status += f"📋 Holdings: {account.get_holdings()}"
    return status

# Create the interface
def create_interface():
    with gr.Blocks(title="Trading Simulation Platform", theme=gr.themes.Soft()) as demo:
        gr.Markdown("# 🏦 Trading Simulation Platform")
        gr.Markdown("Create an account and start trading with simulated stock prices!")
        
        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("## 🆕 Create Account")
                account_id = gr.Textbox(label="Account ID", placeholder="Enter your account ID", value="user123")
                initial_deposit = gr.Slider(0, 10000, step=100, label="Initial Deposit ($)", value=1000)
                create_btn = gr.Button("Create Account", variant="primary")
                create_output = gr.Textbox(label="Account Status", interactive=False, lines=4)
            
            with gr.Column(scale=1):
                gr.Markdown("## 💰 Account Operations")
                deposit_amount = gr.Slider(0, 5000, step=50, label="Deposit Amount ($)", value=0)
                deposit_btn = gr.Button("Deposit", variant="secondary")
                deposit_output = gr.Textbox(label="Deposit Result", interactive=False, lines=3)
                
                withdraw_amount = gr.Slider(0, 5000, step=50, label="Withdraw Amount ($)", value=0)
                withdraw_btn = gr.Button("Withdraw", variant="secondary")
                withdraw_output = gr.Textbox(label="Withdraw Result", interactive=False, lines=3)
        
        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("## 📈 Trading Operations")
                buy_symbol = gr.Textbox(label="Stock Symbol", placeholder="AAPL, TSLA, GOOGL", value="AAPL")
                buy_quantity = gr.Slider(1, 100, step=1, label="Buy Quantity", value=1)
                buy_btn = gr.Button("Buy Shares", variant="secondary")
                buy_output = gr.Textbox(label="Buy Result", interactive=False, lines=4)
                
                sell_symbol = gr.Textbox(label="Stock Symbol", placeholder="AAPL, TSLA, GOOGL", value="AAPL")
                sell_quantity = gr.Slider(1, 100, step=1, label="Sell Quantity", value=1)
                sell_btn = gr.Button("Sell Shares", variant="secondary")
                sell_output = gr.Textbox(label="Sell Result", interactive=False, lines=4)
            
            with gr.Column(scale=1):
                gr.Markdown("## 📊 Portfolio Information")
                portfolio_btn = gr.Button("Get Portfolio Value", variant="secondary")
                portfolio_output = gr.Textbox(label="Portfolio Value", interactive=False, lines=2)
                
                profit_loss_btn = gr.Button("Get Profit/Loss", variant="secondary")
                profit_loss_output = gr.Textbox(label="Profit/Loss", interactive=False, lines=2)
                
                status_btn = gr.Button("Account Status", variant="secondary")
                status_output = gr.Textbox(label="Account Status", interactive=False, lines=6)
                
                history_btn = gr.Button("Transaction History", variant="secondary")
                history_output = gr.Textbox(label="Transaction History", interactive=False, lines=8)
        
        # Stock prices info
        gr.Markdown("### 📊 Current Stock Prices")
        gr.Markdown("- **AAPL**: $150.00")
        gr.Markdown("- **TSLA**: $700.00") 
        gr.Markdown("- **GOOGL**: $2,500.00")
        
        # Event handlers
        create_btn.click(create_account, inputs=[account_id, initial_deposit], outputs=create_output)
        deposit_btn.click(deposit_funds, inputs=deposit_amount, outputs=deposit_output)
        withdraw_btn.click(withdraw_funds, inputs=withdraw_amount, outputs=withdraw_output)
        buy_btn.click(buy_shares, inputs=[buy_symbol, buy_quantity], outputs=buy_output)
        sell_btn.click(sell_shares, inputs=[sell_symbol, sell_quantity], outputs=sell_output)
        portfolio_btn.click(portfolio_value, outputs=portfolio_output)
        profit_loss_btn.click(profit_loss, outputs=profit_loss_output)
        status_btn.click(get_account_status, outputs=status_output)
        history_btn.click(transaction_history, outputs=history_output)
    
    return demo

# Launch the interface
if __name__ == "__main__":
    demo = create_interface()
    demo.launch(share=False, inbrowser=True)