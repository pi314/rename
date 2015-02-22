#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import sys
import re
import os
import argparse

PYTHON_VERSION = sys.version_info[0]

TAG_LEVEL_COLOR = {
    'ok':       '\033[1;32m',
    'error':    '\033[1;31m',
    'warning':  '\033[1;33m',
    'warn':     '\033[1;33m',
    'info':     '',
}

commit_list = []

def tag_message (level, tag, message):
    print( '{}[{:^6}]\033[m {}'.format(TAG_LEVEL_COLOR[level.lower()], tag, message) )

def error_and_exit (message):
    tag_message('error', 'error', message)
    exit()

def main ():
    parser = argparse.ArgumentParser(description='Massive rename tool')

    parser.add_argument('-t', action='store_true', dest='transaction_bit',
                        help='Transaction mode, all tasks will be done together.')

    parser.add_argument('-i', action='store_true', dest='interactive_bit',
                        help='Interactive mode, every task needs user\'s confirm.')

    parser.add_argument('-l', action='store_true', dest='list_action_bit',
                        help='Just show tasks list and do nothing.')

    parser.add_argument('match_pattern', type=str,
                        help='The pattern being replaced.')

    parser.add_argument('replace_pattern', type=str,
                        help='The pattern being replaced to.')

    parser.add_argument('files_list', nargs=argparse.REMAINDER,
                        help='File list')

    args = parser.parse_args()

    print('Match pattern:  {}'.format(args.match_pattern) )
    print('Replace string: {}'.format(args.replace_pattern) )
    print('Files:', ', '.join(args.files_list))

    if args.match_pattern == '':
        error_and_exit('Match pattern cannot be empty string.')

    if os.path.exists(args.match_pattern):
        error_and_exit('Pattern \033[1;33m{}\033[m exists, please use ``mv`` utility instead.'.format(args.match_pattern) )

    if os.path.exists(args.replace_pattern):
        error_and_exit('Pattern \033[1;33m{}\033[m exists, please use ``mv`` utility instead.'.format(args.replace_pattern) )
    
    if args.files_list == []:
        error_and_exit('No files specified')

    print()

    if args.list_action_bit:
        print('Tasks list:')

    for i in args.files_list:
        try:

            if re.search(args.match_pattern, i):

                j = re.sub(args.match_pattern, args.replace_pattern, i)

                if i != j:

                    if args.list_action_bit:
                        tag_message('ok', 'rename', '{} -> {}'.format(i, j) )
                        continue

                    if args.transaction_bit:
                        commit_list.append( (i, j, ) )
                        continue

                    a = 'y'
                    if args.interactive_bit:
                        print('Rename {} to {} [Y/n/t]?'.format(i, j), end=' ')
                        a = input().strip()
                        while a not in ('Y', 'y', 'N', 'n', 'T', 't', ''):
                            print('Rename {} to {} [Y/n/t]?'.format(i, j), end=' ')
                            a = input().strip()

                    if a in ('N', 'n'):
                        tag_message('warning', 'skip', '\033[1;33m{}\033[m canceled\033[m'.format(i) )

                    elif a in ('Y', 'y', ''):
                        os.rename(i, j)
                        tag_message('ok', 'rename', '{} -> {}'.format(i, j) )

                    elif a in ('T', 't'):
                        print('\033[1;32mAdd ({}, {}) into tranaction list\033[m'.format(i, j))
                        commit_list.append( (i,j) )

                else:
                    tag_message('warning', 'skip', '\033[1;33m{}\033[m not changed'.format(i) )

            else:
                tag_message('warning', 'skip', '\033[1;33m{}\033[m not changed'.format(i) )

        except Exception as e:
            print('\033[1;31m'+ str(e) +'\033[m')

    print()

    if args.list_action_bit:
        print('-l argument specified, do nothing, exit')
        exit()

    a = 'y'
    if len(commit_list):
        print('This program will perform the following task:')
        for i in commit_list:
            tag_message('info', 'rename', '{} -> {}'.format(i[0], i[1]) )

        print('Continue? [Y/n]', end=' ')
        a = input().strip()
        while a not in ('Y', 'y', 'N', 'n', ''):
            print('Continue? [Y/n]', end=' ')
            a = input().strip()

        print()

    if a in ('Y', 'y'):
        try:
            for i in commit_list:
                os.rename(i[0], i[1])
                tag_message('ok', 'rename', '{} -> {}'.format(i[0], i[1]) )

        except Exception as e:
            print('\033[1;31m'+ str(e) +'\033[m')

        if len(commit_list):
            print()

    else:
        tag_message('error', 'error', 'Transaction canceled')
        print()

    print('Tasks finished, exit')

if __name__ == '__main__':
    main()

