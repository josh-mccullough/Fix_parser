#! /usr/bin/env python
from pprint import pprint


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
        if value == 'A':
            return "LOGON-MESSAGE"
        return value


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
        message_dict["52"] = message_dict["52"][:4] + '-' + message_dict["52"][4:6] + '-' + message_dict["52"][6:8]\
                             + ' || ' + message_dict["52"][9:]
        return message_dict

    def convert(self, message):
        current_message_dict = self.parse_fix_message_into_dict(message)
        fix_dict = self.create_dict_from_fix_tags()
        converted_dict = {}
        for key in set(fix_dict).intersection(current_message_dict):
            converted_dict[fix_dict.values()[fix_dict.keys().index(key)]] = current_message_dict.values()[current_message_dict.keys().index(key)]
        return converted_dict

    def take_in_messages(self, messages):
        for line in messages:
            print line

if __name__ == "__main__":
    parser = FixParser()
    parser.take_in_messages('8=FIXT.1.19=9835=A49=BME56=DBL52=20170823-08:35:12.40934=150=TID57=SID98=0108=30141=Y')
    message_dict = parser.convert('8=FIXT.1.19=9835=A49=BME56=DBL52=20170823-08:35:12.40934=150=TID57=SID98=0108=30141=Y')
    fix_message_dict = FixDict(message_dict)
    pprint(fix_message_dict)
