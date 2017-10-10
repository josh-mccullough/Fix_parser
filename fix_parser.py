#! /usr/bin/env python
from pprint import pprint
import argparse
import xml.etree.cElementTree as etree
import time

parser = argparse.ArgumentParser(description="Fix log message parser")
parser.add_argument("message_log")
args = parser.parse_args()


# class FixDict(dict):
#
#     def __init__(self, message_dict):
#         """
#        Takes a fix message dict
#        """
#         dict.__init__(self)
#         for k, v in message_dict.iteritems():
#             convert_function_name = "convert_{0}".format(v)
#             attr = getattr(self, convert_function_name, None)
#             if attr is not None:
#                 self[v] = attr(v)
#             else:
#                 self[v] = v
#
#     def convert_MsgType(self, value):
#         return value




class FixParser:

    def __init__(self):
        self.tags = self.store_tags({})
        self.message_dicts = self.take_in_log()
        #pprint(self.message_dicts)

    def store_tags(self, tags):

        doc = etree.parse('FIX50SP2.xml')

        root = doc.getroot()

        fi = root.find('fields')

        for node in fi.getchildren():
            r = node.get("number")
            tags[r] = {}
            tags[r]["name"] = node.get("name")
            for value in node:
                tags[r][value.get("enum")] = value.get("description")

        return tags

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


    def take_in_log(self):
        newlist = []
        with open(args.message_log, 'rb') as input_messages:
            for line in input_messages:
                fix_message_dict = self.parse_fix_message_into_dict(line[24:])
                newlist.append(fix_message_dict)
            return newlist


    def convert(self):
        newlist = []
        for dict in self.message_dicts:
            print dict
            for k, v in dict.iteritems():
                try:
                    if str(v) in self.tags[str(k)]:

                        new_key = self.tags[str(k)]["name"]
                        self.message_dicts[new_key] = self.message_dicts.pop(k)

                        new_value = self.tags[str(k)][str(v)]
                        self.message_dicts[new_value] = self.message_dicts.pop(v)
                    else:
                        new_key = self.tags[str(k)]["name"]
                        self.message_dicts[new_key] = self.message_dicts.pop(k)
                        v = str(v)
                except (KeyError, TypeError) as e:
                    pass
        


if __name__ == "__main__":

    time1 = time.time()
    parser = FixParser()
    parser.convert()
    time2 = time.time()

    print "Execution time: " + str(time2 - time1)


