#!/usr/bin/env python

import xml.etree.cElementTree as etree
import optparse
import json
import sys


class FixParser:

    def __init__(self, dictionary):
        self._dictionary = dictionary
        self._tags = self.store_tags()

    @property
    def tags(self):
        return self._tags

    @property
    def dictionary(self):
        return self._dictionary

    def store_tags(self):
        doc = etree.parse(self.dictionary)
        root = doc.getroot()
        fi = root.find('fields')

        tags = {}
        for node in fi.getchildren():
            r = node.get("number")
            tags[r] = {}
            tags[r]["name"] = node.get("name")
            for value in node:
                tags[r][value.get("enum")] = value.get("description")

        return tags

    def convertToDict(self, message):
        messageDict = dict()
        for k, v in message:
            # convert message-type
            name = k
            value = v
            try:
                definition = self.tags[k]
                name = definition['name']
                value = definition.get(value, value)
            except KeyError:
                print >>sys.stderr, "unknown-tag:", k
                name = k
                value = v
            finally:
                messageDict[name] = value
                
        return messageDict

    def convert(self, output, message):
        converted = self.convertToDict(message)
        encoded = json.dumps(converted, sort_keys=True, indent=4, separators=(',', ': '))
        output.write(encoded + '\n')

    @staticmethod
    def parse_message_log(logFile, delimiter):
        with open(logFile, 'rb') as logFileFd:
            
            messages = []
            for line in logFileFd:
                line = line.rstrip('\n')

                # strip the leading timestamp
                line = line[24:]

                # split by delimiter
                pairs = line.split(delimiter)
                # remove trailing empty element
                del pairs[-1]

                # split by key-value
                pairs = tuple(map(lambda p: tuple(p.split('=')), pairs))
                messages.append(pairs)
                
            return messages
            
            

def main():
    parser = optparse.OptionParser()
    parser.add_option("--output", dest="output",
                      help="Output destination default stdout", default=sys.stdout)
    parser.add_option("--dictionary", dest="dictionary",
                      help="Fix Dictionary", default=None)
    parser.add_option("--delimiter", dest="delimiter",
                      help="Fix Delimiter default \x01", default='\x01')
    options, inputs = parser.parse_args()

    if options.dictionary is None:
        sys.exit('no dictionary specified')

    if len(inputs) == 0:
        sys.exit('no-inputs specified')

    output = open(options.output, 'w') if type(options.output) is not file else options.output
    
    parser = FixParser(options.dictionary)

    for inputLog in inputs:
        inputMessages = FixParser.parse_message_log(inputLog, options.delimiter)
        map(lambda i: parser.convert(output, i), inputMessages)
    
    if type(options.output) is not file:
        output.close()


if __name__ == "__main__":
    main()
