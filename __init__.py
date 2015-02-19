#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import sys
import re
import os
import argparse

PYTHON_VERSION = sys.version_info[0]

commit_list = []

def error_and_exit (message):
    print(message)
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
        error_and_exit('No match pattern specified.')

    if os.path.exists(args.match_pattern):
        error_and_exit('\033[1;31mPattern \033[1;33m{}\033[m \033[1;31mexists, please use ``mv`` utility instead.\033[m'.format(args.match_pattern) )

    if os.path.exists(args.replace_pattern):
        error_and_exit('\033[1;31mPattern \033[1;33m{}\033[m \033[1;31mexists, please use ``mv`` utility instead.\033[m'.format(args.match_pattern) )
    
    if args.files_list == []:
        error_and_exit('No files specified')

    if args.list_action_bit:
        print('Tasks list:')

    try:
        for i in args.files_list:
            j = re.sub(args.match_pattern, args.replace_pattern, i)

            if i != j:

                if args.list_action_bit:
                    print('Rename {} to {}'.format(i, j))
                    continue

                if args.transaction_bit:
                    commit_list.append( (i, j, ) )
                    continue

                a = 'y'
                if args.interactive_bit:
                    print('Rename {} to {} [Y/n/t]?'.format(i, j), end=' ')
                    a = input().strip()
                    while a not in ('Y', 'y', 'N', 'n', 'T', 't', ''):
                        print('rename {} to {}?'.format(i, j), end=' ')
                        a = input().strip()

                if a in ('N', 'n'):
                    print('\033[1;33mRenaming canceled\033[m')

                elif a in ('Y', 'y', ''):
                    print('\033[1;32mRename {} to {}\033[m'.format(i, j))
                    os.rename(i, j)

                elif a in ('T', 't'):
                    print('\033[1;32mAdd ({}, {}) into tranaction list\033[m'.format(i, j))
                    commit_list.append( (i,j) )

            else:
                print( '\033[1;33m{} not changed, skip\033[m'.format(i) )

    except Exception as e:
        print(e)
        exit(1)

    if args.list_action_bit:
        print('-l argument specified, do nothing, exit')

    a = 'y'
    if args.transaction_bit:
        print('This program will perform the following task:')
        for i in commit_list:
            print('Rename {} to {}'.format(i[0], i[1]))

        print('Continue? [Y/n]', end=' ')
        a = input().strip()
        while a not in ('Y', 'y', 'N', 'n', ''):
            print('Continue? [Y/n]', end=' ')
            a = input().strip()

    if a in ('Y', 'y'):
        for i in commit_list:
            os.rename(i[0], i[1])

    else:
        print('\033[1;31mRenaming canceled\033[m')

if __name__ == '__main__':
    main()
