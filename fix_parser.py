#! /usr/bin/env python
from pprint import pprint
import argparse
import xml.etree.cElementTree


parser = argparse.ArgumentParser(description="Fix log message parser")
parser.add_argument("message_log")
args = parser.parse_args()


class FixDict(dict):

    def __init__(self, message_dict):
        """
       Takes a fix message dict
       """
        dict.__init__(self)
        for k, v in message_dict.iteritems():
            convert_function_name = "convert_{0}".format(k)
            global key
            key = k
            attr = getattr(self, convert_function_name, None)
            if attr is not None:
                self[k] = attr(v)
            else:
                self[k] = v

    def convert_MsgType(self, value):
        result = parser.parse_xml(value, key)
        return result

    def convert_AdvSide(self, value):
        result = parser.parse_xml(value, key)
        return result

    def convert_AdvTransType(self, value):
        result = parser.parse_xml(value, key)
        return result

    def convert_CommType(self, value):
        result = parser.parse_xml(value, key)
        return result

    def convert_ExecInst(self, value):
        result = parser.parse_xml(value, key)
        return result

    def convert_HandlInst(self, value):
        result = parser.parse_xml(value, key)
        return result

    def SecurityIDSource(self, value):
        result = parser.parse_xml(value, key)
        return result

    def IOIQltyInd(self, value):
        result = parser.parse_xml(value, key)
        return result

    def IOIQty(self, value):
        result = parser.parse_xml(value, key)
        return result

    def IOITransType(self, value):
        result = parser.parse_xml(value, key)
        return result

    def LastCapacity(self, value):
        result = parser.parse_xml(value, key)
        return result

    def Side(self, value):
        result = parser.parse_xml(value, key)
        return result

    def ExecType(self, value):
        result = parser.parse_xml(value, key)
        return result

    def ExecID(self, value):
        result = parser.parse_xml(value, key)
        return result

    def OrdStatus(self, value):
        result = parser.parse_xml(value, key)
        return result

    def OrdType(self, value):
        result = parser.parse_xml(value, key)
        return result


class FixParser:

    def parse_xml(self, value, keys):
        # TODO get rid of hardcoded xml and replace with an argparse
        your_xml = xml.etree.cElementTree.parse('FIX50SP2.xml').getroot()
        for a_field in your_xml.iter():
            if a_field.tag == "field":
                if a_field.attrib['name'] == keys:
                    for _Values in a_field:
                        if _Values.attrib['enum'] == value:
                            return _Values.attrib['description']

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
        with open(args.message_log, 'rb') as input_messages:
            for line in input_messages:
                fix_message_dict = FixDict(self.convert(line[24:]))
                newlist.append(fix_message_dict)
            pprint(newlist)


if __name__ == "__main__":
    parser = FixParser()
    parser.take_in_log()

