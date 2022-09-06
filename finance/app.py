import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    cash = db.execute("SELECT cash FROM users WHERE id = ?", session.get("user_id"))[0]["cash"]

# STOCKS
# 1 create a dictionary called stocks
    stocks = {}

# 2 create a list with the unique and sorted symbols from the transactions of a given user
    symbollist = db.execute("SELECT DISTINCT symbol FROM transactions WHERE user_id = ? ORDER BY symbol", session.get("user_id"))

# 3 asign the keys to the stocks dictionary from the elements of the stocklist list
    for symbol in symbollist:
        stocks[symbol["symbol"]] = 0

#  4 for each symbol, search in the database all the transactions of the user with that symbol and calculate the current amount of shares, assign that value to the dictionary
    for stock in stocks:
        sharesvalue = 0
        transactions = db.execute(
            "SELECT symbol, shares, type FROM transactions WHERE user_id = ? AND symbol = ? ORDER BY symbol", session.get("user_id"), stock)

# 5 loop in the stocks and drop from the dictionary the pairs which value is 0.0
    # for all the transactions of the user for a given symbol
        for transaction in transactions:
            if transaction["type"] == "buy":
                sharesvalue = sharesvalue + transaction["shares"]
            # else also works here
            elif transaction["type"] == "sell":
                sharesvalue = sharesvalue - transaction["shares"]
            stocks[transaction["symbol"]] = sharesvalue

# TOTAL = sum of every vauel in the dictionary + cash
    stockstotal = 0.0
    for stock in stocks:
        stockstotal = stockstotal + (stocks[stock] * lookup(stock)["price"])
    total = stockstotal


# PRICES dict, in order to render the price data we can make an instant dictionary with the symbols and its current prices
    prices = {}
    for stock in stocks:
        prices[stock] = usd(lookup(stock)["price"])

    print(usd(total))
    return render_template("index.html", cash=usd(cash), stocks=stocks, total=usd(total), prices=prices)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    if request.method == "POST":

        shares = request.form.get("shares")
        print(shares)
        print(shares.isdigit())
        if shares.isdigit() == False:
            return apology("shares should be a number", 400)

        if float(shares) <= 0.0:
            return apology("shares should be higher than 0", 400)

        results = lookup(request.form.get("symbol"))
        if results == None:
            return apology("symbol doesn't exist", 400)

        price = results["price"]
        cost = price * float(shares)
        credit = db.execute("SELECT cash FROM users WHERE id = ?", session.get("user_id"))[0]["cash"]
        if credit >= cost:
            credit = credit - cost

            # create new record in the transactions database
            db.execute("INSERT INTO transactions(user_id, symbol, shares, price, type) VALUES (?, ?, ?, ?, ?)",
                       session.get("user_id"), request.form.get("symbol"), request.form.get("shares"), price, "buy")

            # update the user credit substractig from the total
            db.execute("UPDATE users SET cash = ? WHERE (id = ?)", credit, session.get("user_id"))

            # send user to see his portfolio
            return redirect("/")

        return apology("not enough cash")

    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    history = db.execute("SELECT symbol, shares, price, type FROM transactions WHERE user_id = ?", session.get("user_id"))
    username = db.execute("SELECT username FROM users WHERE id = ?", session.get("user_id"))[0]["username"]
    return render_template("history.html", history=history, name=username)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    if request.method == "POST":

        # Lookup stock symbol
        results = lookup(request.form.get("symbol"))
        # result = lookup(request.form.get("symbol"))
        if results == None:
            return apology("symbol doesn't exist")
        return render_template("quoted.html", token_name=results["name"], token_price=usd(results["price"]), token_symbol=results["symbol"])

    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure confirmation match
        if request.form.get("password") != request.form.get("confirmation"):
            return apology("must coincide", 400)
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure username is not in the database
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        if len(rows) == 1:
            return apology("sorry, username already in use", 400)

        # Include new user and password but the password should be encrypted!!
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", request.form.get(
            "username"), generate_password_hash(request.form.get("password"), "sha256"))
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Log in the user
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    if request.method == "POST":

        shares = float(request.form.get("shares"))
        if shares <= 0.0:
            return apology("shares should be higher than 0")

        results = lookup(request.form.get("symbol"))
        if results == None:
            return apology("symbol doesn't exist")

        # print(db.execute("SELECT DISTINCT symbol FROM transactions WHERE user_id = ?", session.get("user_id")))

        # print(request.form.get("symbol"))
        for pair in db.execute("SELECT DISTINCT symbol FROM transactions WHERE user_id = ?", session.get("user_id")):
            if request.form.get("symbol") == pair["symbol"]:

                # Calculate number of shares (copy from index because stocks is not global)
                stocks = {}
                symbollist = db.execute(
                    "SELECT DISTINCT symbol FROM transactions WHERE user_id = ? ORDER BY symbol", session.get("user_id"))
                for symbol in symbollist:
                    stocks[symbol["symbol"]] = 0
                for stock in stocks:
                    sharesvalue = 0
                    transactions = db.execute(
                        "SELECT symbol, shares, type FROM transactions WHERE user_id = ? AND symbol = ? ORDER BY symbol", session.get("user_id"), stock)
                    for transaction in transactions:
                        if transaction["type"] == "buy":
                            sharesvalue = sharesvalue + transaction["shares"]
                        elif transaction["type"] == "sell":
                            sharesvalue = sharesvalue - transaction["shares"]
                        stocks[transaction["symbol"]] = sharesvalue

                if int(request.form.get("shares")) <= stocks[request.form.get("symbol")]:
                    price = results["price"]
                    cost = price * shares
                    credit = db.execute("SELECT cash FROM users WHERE id = ?", session.get("user_id"))[0]["cash"]

                    credit = credit + cost
                    print("credit B is equal to {}".format(credit))

                    # create new record in the transactions database
                    db.execute("INSERT INTO transactions(user_id, symbol, shares, price, type) VALUES (?, ?, ?, ?, ?)",
                               session.get("user_id"), request.form.get("symbol"), request.form.get("shares"), price, "sell")

                    # update the user credit substractig from the total
                    db.execute("UPDATE users SET cash = ? WHERE (id = ?)", credit, session.get("user_id"))

                    # send user to see his portfolio
                    return redirect("/")

                return apology("you can't sell more shares than you have")

        return apology("you can only sell the stocks you own")
    else:
        return render_template("sell.html", symbollist=db.execute(
            "SELECT DISTINCT symbol FROM transactions WHERE user_id = ? ORDER BY symbol", session.get("user_id")))


@app.route("/deposit", methods=["GET", "POST"])
@login_required
def deposit():
    """Show history of transactions"""
    cash = db.execute("SELECT cash FROM users WHERE id = ?", session.get("user_id"))[0]["cash"]
    if request.method == "POST":
        deposit = request.form.get("deposit")
        if int(deposit) > 0:
            cash = cash + int(deposit)
            db.execute("UPDATE users SET cash = ? WHERE id = ?", cash, session.get("user_id"))
            return redirect("/")
        return apology("deposit a valid amount")

    return render_template("deposit.html", cash=round(cash, 2))


@app.route("/withdraw", methods=["GET", "POST"])
@login_required
def withdraw():
    """Show history of transactions"""
    cash = db.execute("SELECT cash FROM users WHERE id = ?", session.get("user_id"))[0]["cash"]
    if request.method == "POST":
        withdraw = request.form.get("withdraw")
        print(withdraw)
        print(cash)
        if int(withdraw) > 0 and int(withdraw) <= cash:
            cash = cash - int(withdraw)
            db.execute("UPDATE users SET cash = ? WHERE id = ?", cash, session.get("user_id"))
            return redirect("/")
        return apology("withdraw a valid amount")

    return render_template("withdraw.html", cash=round(cash, 2))