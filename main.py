
from operations import Stocks

'''
The main function. Parse the command line parameters,
:param argv: arguments from the command line
'''

option = 0
while True:
    print("---------------------------------------")
    option = input("Enter the number of the Option you want:" +
                       "\n----------------------------------------" +
                       "\n| 1 | Calculate dividend yield" +
                       "\n| 2 | Calculate the P/E Ratio"
                       "\n| 3 | Record Trade" +
                       "\n| 4 | Calculate Volume Weighted Stock Price "
                       "\n| 5 | Calculate the GBCE All Share Index"
                       "\n| 6 | To quit\n" +
                       "----------------------------------------\n>")

    if option == '6':
        break
    elif(option == '1'):
        symbol = input("Choose a stock symbol:" +
                           "\n| 1 | TEA " +
                           "\n| 2 | POP " +
                           "\n| 3 | ALE " +
                           "\n| 4 | GIN " +
                           "\n| 5 | JOE \n" +
                           "----------------------------------------\n>")

        price = input("Enter the stock price \n")
        print("-------------")

        status_code, div_value = Stocks().divident(symbol, price)

        print("Dividend Yield : {0}".format(div_value))

        print("********************************************")
        print("\n \n")

    elif(option == '2'):
        symbol = input("Choose a stock symbol:" +
                           "\n| 1 | TEA " +
                           "\n| 2 | POP " +
                           "\n| 3 | ALE " +
                           "\n| 4 | GIN " +
                           "\n| 5 | JOE \n" +
                           "----------------------------------------\n>")

        price = input("Enter the stock price \n")
        print("-------------")

        status_code, pe_value = Stocks().pe_ratio(symbol, price)

        print("P/E Ratio : {0}".format(pe_value))

        print("********************************************")
        print("\n \n")

    elif(option == '3'):
        symbol = input("Choose a stock symbol:" +
                           "\n| 1 | TEA " +
                           "\n| 2 | POP " +
                           "\n| 3 | ALE " +
                           "\n| 4 | GIN " +
                           "\n| 5 | JOE \n" +
                           "----------------------------------------\n>")

        quantity = input("Quantity of shares \n")

        indicator = input("Choose a indicator :" +
                              "\n| 1 | BUY " +
                              "\n| 2 | SELL \n" +
                              "----------------------------------------\n>")

        traded_price = input("Enter traded price \n")

        print("----------------------------")

        Stocks().record_trade(symbol, quantity, indicator, traded_price)

        print("********************************************")
        print("\n \n")

    elif(option == '4'):
        symbol = input("Choose a stock symbol:" +
                           "\n| 1 | TEA " +
                           "\n| 2 | POP " +
                           "\n| 3 | ALE " +
                           "\n| 4 | GIN " +
                           "\n| 5 | JOE \n" +
                           "----------------------------------------\n>")

        print("-------------")

        Stocks().stock_price(symbol)

        print("********************************************")
        print("\n \n")

    elif(option == '5'):
        Stocks().share_index()

        print("********************************************")
        print("\n \n")
