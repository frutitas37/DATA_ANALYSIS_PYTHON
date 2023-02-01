"""CSC 161 Project: Milestone III

Amii Matamoros Delgado
Lab Section MW 3:25-4:40pm
Spring 2022
"""


def test_data(filename, col, day):
    """A test function to query the data you loaded into your program.

     Args:
        filename: A string for the filename containing the stock data,
                  in CSV format.

        col: A string of either "date", "open", "high", "low", "close",
             "volume", or "adj_close" for the column of stock market data to
             look into.

             The string arguments MUST be LOWERCASE!

        day: An integer reflecting the absolute number of the day in the
             data to look up, e.g. day 1, 15, or 1200 is row 1, 15, or 1200
             in the file.

     Returns:
        A value selected for the stock on some particular day, in some
        column col. The returned value *must* be of the appropriate type,
        such as float, int or str.
    """
    return cvs_23(filename, col, day)


def cvs_23(filename, col, day):
    infile = open(filename, "r")
    lines = infile.readline()
    lines = lines.split(",")
    data = []

    prices = infile.readlines()
    for i in prices:
        specific = i.split(",")
        specific[6] = specific[6].strip()
        data.append(specific)

    dates = day - 1
    if col == "open":
        return float(data[dates][1])
    elif col == "high":
        return float(data[dates][2])
    elif col == "low":
        return float(data[dates][3])
    elif col == "close":
        return float(data[dates][4])
    elif col == "adj_close":
        return float(data[dates][5])
    elif col == "volume":
        return int(data[dates][6])
    elif col == "date":
        return str(data[dates][0])


def transact(funds, stocks, qty, price, buy=False, sell=False):
    """A bookkeeping function to help make stock transactions.

       Args:
           funds: An account balance, a float; it is a value of how much money
           you have, currently.

           stocks: An int, representing the number of stock you currently own.

           qty: An int, representing how many stock you wish to buy or sell.

           price: An float reflecting a price of a single stock.

           buy: This option parameter, if set to true, will initiate a buy.

           sell: This option parameter, if set to true, will initiate a sell.

       Returns:
           Two values *must* be returned. The first (a float) is the new
           account balance (funds) as the transaction is completed. The second
           is the number of stock now owned (an int) after the transaction is
           complete.

           Error condition #1: If the `buy` and `sell` keyword parameters
           are both set to true, or both false. You *must* raise an
           ValueError exception with an appropriate error message since this
           is an ambiguous transaction.

           Error condition #2: If you buy, or sell without enough funds or
           stocks to sell, respectively.  You *must* raise an
           ValueError exception with an appropriate error message since this
           is an ambiguous transaction.
    """
    funds = float(funds)
    stocks = int(stocks)
    qty = int(qty)
    price = float(price)

    if (buy is True) and (sell is True):
        raise ValueError("Ambiguous transaction! Can't determine whether to "
                         "buy or sell!")
    elif (buy is False) and (sell is False):
        raise ValueError("Ambiguous transaction! Can't determine whether to "
                         "buy or sell!")
    elif buy is True and sell is False:
        if(funds < (qty * price)):
            raise ValueError(f"Insufficient funds to purchase {qty} stock "
                             "at ${price:0.2f}!")
        else:
            funds = float(funds - (qty * price))
            stocks = int(stocks + qty)

    elif sell is True and buy is False:
        if(stocks < qty):
            raise ValueError(f"Insufficient stock owned to sell {qty} "
                             "stocks!")
        else:
            funds = float(funds + (qty * price))
            stocks = int(stocks - qty)
    return funds, stocks


def alg_moving_average(filename):
    """This function implements the moving average stock trading algorithm.

    The CSV stock data should be loaded into your program; use that data to
    make decisions using the moving average algorithm.

    Any bookkeeping setup from Milestone I should be called/used here.

    Algorithm:
    - Trading must start on day 21, taking the average of the previous 20 days.
    - You must buy shares if the current day price is 5%, or more, lower
      than the moving average.
    - You must sell shares if the current day price is 5%, or more, higher,
      than the moving average.
    - You must buy, or sell 10 stocks, or less per transaction.
    - You are free to choose which column of stock data to use (open, close,
      low, high, etc)
    - When your algorithm reaches the last day of data, have it sell all
      remaining stock. Your function will return the number of stocks you
      own (should be zero, at this point), and your cash balance.
    - Choose any stock price column you wish for a particular day you use
      (whether it's the current day's "open", "close", "high", etc)

    Args:
        A filename, as a string.

    Returns:
        Note: You *must* sell all your stock before returning.
        Two values, stocks and balance OF THE APPROPRIATE DATA TYPE.

    Prints:
        Nothing.
    """
    infile = open(filename, "r")
    lines = infile.readlines()
    date = len(lines)
    open_ = []
    for y in range(date):
        line = lines[y]
        columns = line.split(",")
        open_ += [columns[1]]

    cash_balance = 1000
    stocks_owned = 0
    x = 0
    for d in range(date):
        if d >= 21:
            avr = 0
            a = 0
            x += 1
            for i in range(20):
                a += float(open_[i + x])
            avr = a / 20
            current = float(open_[d])
            if current <= avr * 0.95 and cash_balance >= current * 10:
                cash_balance, stocks_owned = transact(cash_balance,
                                                      stocks_owned, 10,
                                                      current, buy=True)
            elif current >= avr * 1.05 and stocks_owned >= 10:
                cash_balance, stocks_owned = transact(cash_balance,
                                                      stocks_owned, 10,
                                                      current, sell=True)
        if d == (date - 1):
            cash_balance, stocks_owned = transact(cash_balance, stocks_owned,
                                                  stocks_owned, current,
                                                  sell=True)
    return stocks_owned, cash_balance


def alg_rsi(filename_1, filename_2):
    """This function implements the Relative Strength Index algorithm.

    Using the CSV stock data from two stock files that are loaded into your
    program, use that data to make decisions using the Relative Strength
    Index (RSI) algorithm.

    Algorithm:
        The function makes decision to sell 10 stocks when the RSI > 70
        and buy 10 stocks when the RSI < 30. The number of stocks acquired
        are stored into the variables stocks_owned1 and stocks_owned2,
        and then both are sold at the end. 

    Arguments:
        filename_1 (str): A filename, as a string, for one set of stock
                          data for a first company.

        filename_2 (str): A filename, as a string, for one set of stock
                          data for a second company.

    Returns:
        Two values, stocks and balance OF THEx APPROPRIATE DATA TYPE.

    Prints:
        Nothing.
    """
    infile = open(filename_1)
    infile2 = open(filename_2)
    lines = infile.readlines()
    lines2 = infile2.readlines()
    date = len(lines)
    open_ = []
    open2_ = []
    for y in range(date):
        line = lines[y]
        line2 = lines2[y]
        columns = line.split(",")
        columns2 = line2.split(",")
        open_ += [columns[1]]
        open2_ += [columns2[1]]
    cash_balance = 10000
    stocks_owned1 = 0
    stocks_owned2 = 0
    for d in range(15, date):
        gains = 0
        gains2 = 0
        losses = 0
        losses2 = 0
        for k in range(d-14, d-1):
            price1 = float(open_[k+1])
            price2 = float(open2_[k+1])
            past_price = float(open_[k])
            past_price2 = float(open2_[k])
            if price1 > past_price:
                gains += price1 - past_price
            if price2 > past_price2:
                gains2 += price2 - past_price2
            if price1 < past_price:
                losses += past_price - price1
            if price2 < past_price2:
                losses2 += past_price2 - price2
        averagegain1 = gains / 14
        averageloss1 = losses / 14
        averagegain2 = gains2 / 14
        averageloss2 = losses2 / 14
        if averageloss1 == 0:
            rsi1 = 100
        else:
            rsi1 = 100 - (100 / (1 + (averagegain1 / averageloss1)))
        if averageloss2 == 0:
            rsi2 = 100
        else:
            rsi2 = 100 - (100 / (1 + (averagegain2 / averageloss2)))
        current1 = float(open_[d])
        current2 = float(open2_[d])
        if rsi1 > 70:
            if stocks_owned1 >= 10:
                cash_balance, stocks_owned1 = transact(cash_balance,
                                                       stocks_owned1, 10,
                                                       current1, sell=True)
        if rsi2 > 70:
            if stocks_owned2 >= 10:
                cash_balance, stocks_owned2 = transact(cash_balance,
                                                       stocks_owned2, 10,
                                                       current2, sell=True)
        if rsi1 < 30:
            if cash_balance >= current1 * 10:
                cash_balance, stocks_owned1 = transact(cash_balance,
                                                       stocks_owned1, 10,
                                                       current1, buy=True)
        if rsi2 < 30:
            if cash_balance >= current2 * 10:
                cash_balance, stocks_owned2 = transact(cash_balance,
                                                       stocks_owned2, 10,
                                                       current2, buy=True)
        if d == (date - 1):
            cash_balance, stocks_owned1 = transact(cash_balance, stocks_owned1,
                                                   stocks_owned1, current1,
                                                   sell=True)
            cash_balance, stocks_owned2 = transact(cash_balance, stocks_owned2,
                                                   stocks_owned2, current2,
                                                   sell=True)
    return (stocks_owned1 + stocks_owned2), float(cash_balance)


def main():
    stock_file_1 = input("Enter a filename for stock data (in CSV format): ")
    alg1_stocks, alg1_balance = alg_moving_average(stock_file_1)
    print("The results are", alg1_stocks, alg1_balance)
    stock_file_2 = input("Enter another filename for second stock data "
                         "file (in CSV format): ")
    alg2_stocks, alg2_balance = alg_rsi(stock_file_1, stock_file_2)
    print("The results are...", alg2_stocks, alg2_balance)


if __name__ == '__main__':
    main()
