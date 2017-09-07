#! /usr/bin/env python
from pprint import pprint
import argparse


class FixDict(dict):

    def __init__(self, message_dict):
        """
       Takes a fix message dict
       """
        dict.__init__(self)
        for k, v in message_dict.iteritems():
            convert_function_name = "convert_{0}".format(k)
            attr = getattr(self, convert_function_name, None)
            if attr is not None:
                self[k] = attr(v)
            else:
                self[k] = v

    def convert_MsgType(self, value):
        # TODO parse in an xml here maybe? or a dict to iterate over and if the value appears then change it
        if value == 'A':
            return "LOGON-MESSAGE"
        if value == '0':
            return 'Heartbeat'
        if value == '8':
            return 'Execution Report'
        return value

    def convert_OrdType(self, value):
        if value == '1':
            return 'Market'
        if value == '2':
            return 'Limit'
        return value

    def convert_AccountType(self, value):
        if value == '1':
            return 'Account carried on customer side of books'
        if value == '2':
            return 'Account carried on non-customer side of books'
        if value == '3':
            return 'House Trader'
        if value == '4':
            return 'Floor Trader'
        if value == '6':
            return 'Account is carried on non-customer side of books and is cross margined'
        if value == '7':
            return 'Account is house trader and is cross margined'
        if value == '8':
            return 'Joint Back office Account (JBO)'
        return value

    def convert_ExecType(self, value):
        if value == '0':
            return 'NEW'
        if value == '3':
            return 'DONE_FOR_DAY'
        if value == '4':
            return 'CANCELLED'
        if value == '5':
            return 'REPLACED'
        if value == '6':
            return 'PENDING_CANCEL'
        if value == '7':
            return 'STOPPED'
        if value == '8':
            return 'REJECTED'
        if value == '9':
            return 'SUSPENDED'
        if value == 'A':
            return 'PENDING_NEW'
        if value == 'B':
            return 'CALCULATED'
        if value == 'C':
            return 'EXPIRED'
        if value == 'D':
            return 'RESTARTED'
        if value == 'E':
            return 'PENDING_REPLACE'
        if value == 'F':
            return 'TRADE'
        if value == 'G':
            return 'TRADE_CORRECT'
        if value == 'H':
            return 'TRADE_CANCEL'
        if value == 'I':
            return 'ORDER_STATUS'
        if value == 'J':
            return 'TRADE_IN_A_CLEARING_HOLD'
        if value == 'K':
            return 'TRADE_HAS_BEEN_RELEASED_TO_CLEARING'
        if value == 'L':
            return 'TRIGGERED_OR_ACTIVATED_BY_SYSTEM'


class FixParser:

    def create_dict_from_fix_tags(self):
        """Reads in from list of FIX tags, then stores the tags and explanations as key and value in dict"""
        file = open("FIX5.0-Tags.txt", "r")
        fix_tags = {}
        for l in file:
            fix_tags[l.split()[0]] = l.split()[1]  # Places the content of each line into a dictionary
        file.close()
        return fix_tags  # Returns a dictionary containing all FIX tags

    def parse_fix_message_into_dict(self, fix_message):
        ''' This will take in a fix message and convert it into a dictionary so i can comapre it with the dict of
            tags I have  '''
        l = []
        message_dict = {}
        l = fix_message.split('\x01')  # Removes separator characters
        del l[-1]  # Removes \n
        for c in l:
            message_dict[c.split("=")[0]] = c.split("=")[1]  # Splits each element into key and value
        return message_dict

    def convert(self, message):
        current_message_dict = self.parse_fix_message_into_dict(message)
        fix_dict = self.create_dict_from_fix_tags()
        converted_dict = {}
        for key in set(fix_dict).intersection(current_message_dict):
            converted_dict[fix_dict.values()[fix_dict.keys().index(key)]] = current_message_dict.values()[current_message_dict.keys().index(key)]
        return converted_dict

    def take_in_log(self):
        newlist = []

        parser = argparse.ArgumentParser(description="Fix log message parser")
        parser.add_argument("message_log")
        args = parser.parse_args()

        with open(args.message_log, 'rb') as input_messages:
            for line in input_messages:
                fix_message_dict = FixDict(self.convert(line[24:]))
                newlist.append(fix_message_dict)
            pprint(newlist)


if __name__ == "__main__":
    parser = FixParser()
    parser.take_in_log()
