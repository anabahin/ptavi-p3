#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import json
from xml.sax import make_parser
from urllib.request import urlretrieve
from smallsmilhandler import SmallSMILHandler

usage_error = 'usage error: python3 karaoke.py <file.smil>'

def smil2json(filename, tag_list):

    with open(filename.replace('smil','json'), 'w') as smil_file:
        json.dump(tag_list, smil_file, indent=3)

def print_tags(tag_list):

    tags_str = ''

    for tag in tag_list:
        tags_str += tag[0]
        for att in tag[1]:
            if tag[1][att] != '':
                tags_str += '\t' + att + '="' + tag[1][att] + '"'
        tags_str += '\n'

    print(tags_str)

def download_files(filename, tag_list):

    for tag in tag_list:
        for att in tag[1]:
            if 'http://' in tag[1][att]:
                name = tag[1][att].split('/')[-1]
                urlretrieve(tag[1][att], name)
                tag[1][att] = name

    smil2json(filename, tag_list)

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

    parser = make_parser()
    SMILHandler = SmallSMILHandler(att_list)
    parser.setContentHandler(SMILHandler)
    parser.parse(open(filename))

    tags = SMILHandler.get_tags()
    smil2json(filename, tags)
    print_tags(tags)
    download_files(filename, tags)
    print_tags(tags)
