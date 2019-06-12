#!/usr/bin/python3
# -*- coding: utf-8 -*-

from xml.sax import make_parser
from xml.sax.handler import ContentHandler

class SmallSMILHandler(ContentHandler):

    def __init__ (self, att_list):

        self.tag_list = []
        self.att_list = att_list

    def startElement(self, name, attrs):

        dicc = {}
        if name in self.att_list:
            for att in self.att_list[name]:
                dicc[att] = attrs.get(att, '')
            self.tag_list.append([name, dicc])

    def get_tags(self):

        return self.tag_list


if __name__ == '__main__':

    att_list = {'root-layout': ['width', 'height', 'background-color'],
                'region': ['id', 'top', 'bottom', 'left', 'right'],
                'img': ['src', 'region', 'begin', 'dur'],
                'audio': ['src', 'begin', 'dur'],
                'textstream': ['src', 'region']}

    parser = make_parser()
    SMILHandler = SmallSMILHandler(att_list)
    parser.setContentHandler(SMILHandler)
    parser.parse(open('karaoke.smil'))

    print(SMILHandler.get_tags())
