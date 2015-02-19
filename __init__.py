#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import sys
import re
import os

PYTHON_VERSION = sys.version_info[0]

transaction_bit = False
interactive_bit = False

match_pattern   = ''
replace_pattern = ''

files_list = []
commit_list = []

def parse_argument ():
    global transaction_bit
    global interactive_bit
    global match_pattern
    global replace_pattern
    global files_list
    global commit_list

    argv = sys.argv[1:]
    while len(argv) > 0:
        if argv[0].startswith('-'):
            for i in argv[0]:

                if i in('t'):
                    transaction_bit = True

                elif i in ('i'):
                    interactive_bit = True

            argv = argv[1:]
            continue

        if match_pattern == '':
            match_pattern = argv[0]
            if os.path.exists(argv[0]):
                print('\033[1;31mPattern \033[1;33m{}\033[m '.format(argv[0]), end='')
                print('\033[1;31mexists, please use ``mv`` utility instead.\033[m')
                exit()

        elif replace_pattern == '':
            replace_pattern = argv[0]
            if os.path.exists(argv[0]):
                print('\033[1;31mPattern \033[1;33m{}\033[m '.format(argv[0]), end='')
                print('\033[1;31mexists, please use ``mv`` utility instead.\033[m')
                exit()

        else:
            files_list.append(argv[0])

        argv = argv[1:]

def error_and_exit (message):
    print(message)
    exit()

def main ():
    parse_argument()
    print('Match pattern: ', match_pattern)
    print('Replace string:', replace_pattern)
    print('Files:         ', ', '.join(files_list))

    if match_pattern == '':
        error_and_exit('No match pattern specified.')
    
    if files_list == []:
        error_and_exit('No files specified')

    try:
        for i in files_list:
            j = re.sub(match_pattern, replace_pattern, i)
            if i != j:
                if transaction_bit:
                    commit_list.append( (i, j, ) )
                    continue

                a = 'y'
                if interactive_bit:
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
                print( '\033[1;33m{} does not match pattern, skip\033[m'.format(i) )

    except Exception as e:
        print(e)
        exit(1)

    a = 'y'
    if transaction_bit:
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
