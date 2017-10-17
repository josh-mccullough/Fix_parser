#!/usr/bin/env python

import xml.etree.cElementTree as etree
import optparse
import logging
import json
import sys
import os


logger = logging.getLogger('FIX-PARSER')


class FixParser:

    def __init__(self, dictionary):
        self._dictionary = dictionary
        self._tags = self._parse_dictionary()

    @property
    def tags(self):
        return self._tags

    @property
    def dictionary(self):
        return self._dictionary

    def _parse_dictionary(self):
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
                logger.warning("unknown-tag: {0}={1}".format(k,v))
            finally:
                messageDict[name] = value
                
        return messageDict

    def convert(self, output, message):
        converted = self.convertToDict(message)
        encoded = json.dumps(converted, sort_keys=True, indent=4, separators=(',', ': '))
        output.write(encoded + '\n')

    @staticmethod
    def parse_raw_message(rawMessage, delimiter):
        pairs = rawMessage.split(delimiter)
        
        # remove trailing pair
        if len(pairs[-1]) == 0:
            del pairs[-1]
        
        return tuple(map(lambda p: tuple(p.split('=')), pairs))

    @staticmethod
    def parse_message_log(logFile, delimiter):
        with open(logFile, 'rb') as logFileFd:
            
            messages = []
            for line in logFileFd:
                line = line.rstrip('\n')

                # strip the leading timestamp
                line = line[24:]

                pairs = FixParser.parse_raw_message(line, delimiter)
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

    for inp in inputs:
        isPipe = inp == '-'
        isFile = os.path.exists(inp)
        
        inputMessages = None
        if isPipe:
            inputMessages = map(lambda l: FixParser.parse_raw_message(l.strip('\n'), options.delimiter), sys.stdin)
        elif isFile:
            inputMessages = FixParser.parse_message_log(inp, options.delimiter)
        else:
            inputMessages = [FixParser.parse_raw_message(inp, options.delimiter)]
            
        map(lambda i: parser.convert(output, i), inputMessages)
    
    if type(options.output) is not file:
        output.close()


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
    main()
