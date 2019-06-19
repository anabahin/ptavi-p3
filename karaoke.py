#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import json
from xml.sax import make_parser
from urllib.request import urlretrieve
from smallsmilhandler import SmallSMILHandler

usage_error = 'usage error: python3 karaoke.py <file.smil>'


class KaraokeLocal:

    def __init__(self, filename, att_list):
        parser = make_parser()
        SMILHandler = SmallSMILHandler(att_list)
        parser.setContentHandler(SMILHandler)
        parser.parse(open(filename))

        self.tag_list = SMILHandler.get_tags()

    def __str__(self):
        tags_str = ''

        for tag in self.tag_list:
            tags_str += tag[0]
            for att in tag[1]:
                if tag[1][att] != '':
                    tags_str += '\t' + att + '="' + tag[1][att] + '"'
            tags_str += '\n'

        return tags_str

    def do_local(self):
        for tag in self.tag_list:
            for att in tag[1]:
                if 'http://' in tag[1][att]:
                    name = tag[1][att].split('/')[-1]
                    urlretrieve(tag[1][att], name)
                    tag[1][att] = name

    def to_json(self, filesmil, filejson=''):
        if filejson:
            with open(filejson, 'w') as jsonfile:
                json.dump(self.tag_list, jsonfile, indent=3)
        else:
            with open(filesmil.replace('smil', 'json'), 'w') as jsonfile:
                json.dump(self.tag_list, jsonfile, indent=3)


if __name__ == '__main__':

    if len(sys.argv) != 2:
        sys.exit(usage_error)
    else:
        filename = sys.argv[1]

    att_list = {'root-layout': ['width', 'height', 'background-color'],
                'region': ['id', 'top', 'bottom', 'left', 'right'],
                'img': ['src', 'region', 'begin', 'dur'],
                'audio': ['src', 'begin', 'dur'],
                'textstream': ['src', 'region']}

    karaoke = KaraokeLocal(filename, att_list)

    print(karaoke)
    karaoke.to_json(filename)
    karaoke.do_local()
    karaoke.to_json(filename, 'local.json')
    print(karaoke)
