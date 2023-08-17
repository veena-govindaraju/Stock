import csv
import json
import os

from bson import json_util
from datetime import datetime, timedelta

stock_mapping = {
    1: "TEA",
    2: "POP",
    3: "ALE",
    4: "GIN",
    5: "JOE"
}

indicator_mapping = {
    1: "BUY",
    2: "SELL"

}

gbce_csv_reader = list(csv.DictReader(open('gbce.csv')))


class TradeRecord():
    '''
        Class for Record Trade data
    
    '''

    def __init__(self, symbol, quantity, indicator, traded_price, created_time):
        self.symbol = symbol
        self.quantity = quantity
        self.indicator = indicator
        self.traded_price = traded_price
        self.created_time = created_time

    def trade_details(self):
        data = {}
        data["Symbol"] = self.symbol
        data["Quantity"] = self.quantity
        data["Indicator"] = self.indicator
        data["Trade Price"] = self.traded_price
        data["Created Time"] = self.created_time
        return data


class Stocks():

    @classmethod
    def divident(self, symbol, price):
        '''
            Dividend yield for given stock.
            The initial data about the dividends are static taken from csv file.

            :param symbol: of the stock
            :param price: price.
            :return: value or throw a Error msg if symbol not registered or the price is not valid
        '''

        stock_symbol = stock_mapping.get(int(symbol), None)

        if stock_symbol is None:
            return False, "Enter Valid Stock Symbol"

        try:
            if float(price) == 0.0:
                return False, "Enter valid price"
        except:
            return False, "Enter valid price"

        for gbce_stock in gbce_csv_reader:
            if gbce_stock['stock_symbol'] == str(stock_symbol):
                if gbce_stock['stock_type'] == "Common":
                    try:
                        divident = float(gbce_stock.get('last_divident', 0)) / float(price)
                    except ZeroDivisionError:
                        divident = 0
                else:
                    try:
                        divident = (float(gbce_stock.get('fixed_divident', 0))/100) * \
                            float(gbce_stock.get('par_value', 0)) / float(price)
                    except ZeroDivisionError:
                        divident = 0

                return True, divident

    @classmethod
    def pe_ratio(self, symbol, price):
        '''
            P/E Ratio for given stock.
            The initial data about the dividends are static taken from csv file.
            :param symbol: of the stock
            :param price : given price
            :return: value
        '''

        status_code, result = self.divident(symbol, price)

        if not status_code:
            return status_code, result
        else:
            try:
                pe_ratio = float(price) / float(result)
            except ZeroDivisionError:
                pe_ratio = 0

            return True, pe_ratio

    @classmethod
    def record_trade(self, symbol, quantity, indicator, traded_price):
        '''
            Record a new trade in the stock.

            :param symbol: of the stock
            :param indicator: SELL, BUY
            :param quantity: to trade
            :param traded_price: price of the trade
        '''

        trade_record_file = open("trade_record_file", "r")

        is_file_empty = os.path.getsize("trade_record_file") == 0

        if not is_file_empty:
            list_trade_records = trade_record_file.readlines()
        else:
            list_trade_records = []

        stock_symbol = stock_mapping.get(int(symbol), None)
        quantity = int(quantity)
        indicator = indicator_mapping.get(int(indicator), None)
        traded_price = float(traded_price)

        try:
            trade_record_data = TradeRecord(stock_symbol, quantity, indicator, traded_price, datetime.now())

            trade_record_file = open("trade_record_file", "w")
            list_trade_records.append(json.dumps(trade_record_data.trade_details(), default=json_util.default))
            list_trade_records.append("\n")
            print("Value of trade_record_data : {0} and value : {1}".format(trade_record_data, list_trade_records))
            trade_record_file.writelines(list_trade_records)
            print("Trade_record {0}".format(trade_record_data.trade_details()))
            print("----------------------------")
            print("Trade data Recorded !!! ")
        except KeyboardInterrupt:
            print("----------------------------")
            print("Trade data Not Added")
        except EOFError:
            print("----------------------------")
            print("Trade data Not Added")
        finally:
            trade_record_file.close()

    @classmethod
    def stock_price(self, symbol):
        '''
            Calculate stock price for given stock based on trades from last 15 min.

            :param symbol: of the stock
            :return: value

        '''

        stock_symbol = stock_mapping.get(int(symbol), None)
        trade_time = datetime.now() - timedelta(minutes=15)

        trade_record_file = open("trade_record_file", "r")

        is_file_empty = os.path.getsize("trade_record_file") == 0

        quantity_sum = 0
        sum_trade_price = 0

        if not is_file_empty:
            list_trade_records = trade_record_file.readlines()

            for trade_record in list_trade_records:
                trade_record = json.loads(trade_record, object_hook=json_util.object_hook)
                if trade_record["Symbol"] == stock_symbol and trade_record["Created Time"] >= trade_time:
                    print("Trade_record {0}".format(trade_record))
                    quantity_sum += trade_record["Quantity"]
                    sum_trade_price += (trade_record["Quantity"] * trade_record["Trade Price"])

            if sum_trade_price and quantity_sum:
                vol_weight_stock_price = sum_trade_price/quantity_sum
                print("----------------------------")
                print("Volume Weighted Stock Price :  {0}".format(float(vol_weight_stock_price)))

            else:
                return "Trade record is empty for the stock {0} in the past 15 minutes".format(stock_symbol)

        else:
            print("----------------------------")
            print("Trade Record is empty")

    @classmethod
    def share_index(self):
        '''
            Calculate the GBCE All Share Index using the geometric mean of prices
            for all stocks.

            :return: value
        '''

        trade_time = datetime.now() - timedelta(minutes=15)

        trade_record_file = open("trade_record_file", "r")

        is_file_empty = os.path.getsize("trade_record_file") == 0

        quantity_sum = 0
        sum_trade_price = 0

        if not is_file_empty:
            list_trade_records = trade_record_file.readlines()

            for trade_record in list_trade_records:
                trade_record = json.loads(trade_record, object_hook=json_util.object_hook)
                if trade_record["Created Time"] >= trade_time:
                    print("trade_record {0}".format(trade_record))
                    quantity_sum += trade_record["Quantity"]
                    sum_trade_price += (trade_record["Quantity"] * trade_record["Trade Price"])

            if sum_trade_price and quantity_sum:
                gbce_share_index = sum_trade_price**(1/quantity_sum)
                print("----------------------------")
                print("GBCE Share Index :  {0}".format(float(gbce_share_index)))

            else:
                return "Trade Record is empty"

        else:
            print("----------------------------")
            print("Trade Record is empty")