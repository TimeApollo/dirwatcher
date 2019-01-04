#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""Dirwatcher program.

Long Running Program that monitors a directory for certain files and a magic
word in the directory.
The program will continue to run unless sent a signal to terminate.
All other errors will be handled with exceptions and logged and
the program will continue running.

Author: Aaron Jackson
Github: TimeApollo
"""
__author__ = 'Aaron '

import argparse
import logging
import signal
import time
import datetime
import os
from functools import partial

exit_flag = False


def find_magic_text(directory, ext, text, file_dict, logger):
    """Searches directory for magic text."""
    files = os.listdir(directory)
    for file in files:
        if os.path.splitext(file)[1] == ext:
            if file not in file_dict:
                file_dict[file] = 0
    files_to_del = []
    for file in file_dict:
        try:
            with open(os.path.join(directory, file), 'r') as f:
                content = [line.rstrip() for line in f]
                for i, line in enumerate(content, 1):
                    if i > file_dict[file]:
                        if text in line:
                            logger.info('Magic text "{}" found in file {} on line {}'.format(text, file, i))
                            file_dict[file] = i
        except IOError:
            logger.warn('{} file deleted from directory.'.format(file))
            files_to_del.append(file)
        except Exception as e:
            logger.error('UnCaught exception: {}: {}'.format(type(e).__name__, e))
    for file in files_to_del:
        file_dict.pop(file, None)


def sig_handler(logger, sig_num, frame):
    """Handles OS signals SIGTERM and SIGINT."""
    global exit_flag
    sigs = dict((k, v) for v, k in reversed(sorted(signal.__dict__.items()))
                if v.startswith('SIG') and not v.startswith('SIG_'))
    logger.warn('Received OS Signal: {}'.format(sigs[sig_num]))

    # only exit if it is a sigterm or sigint
    if sig_num == signal.SIGINT or sig_num == signal.SIGTERM:
        exit_flag = True


def format_ext(ext):
    """Formats extension with a . infront."""
    if ext.startswith('.'):
        return ext
    else:
        return '.' + ext


def dirwatcher(parser, logger):
    """Dirwatcher program main logic."""
    # handlers for SIGINT and SIGTERM
    signal.signal(signal.SIGINT, partial(sig_handler, logger))
    signal.signal(signal.SIGTERM, partial(sig_handler, logger))

    # Values from parser.
    directory, ext = parser.dir, parser.ext
    interval, text = parser.int, parser.text
    # ensures a . infront of ext string
    ext = format_ext(ext)
    file_dict = {}

    while not exit_flag:
        print(os.getcwd())
        if not os.path.isdir(directory):
            logger.warn('Directory {} does not exist!'.format(directory))
        else:
            try:
                # files = os.listdir(directory)
                find_magic_text(directory, ext, text, file_dict, logger)
            except OSError as e:
                if e.errno == os.errno.ENOENT:
                    logger.warn('Directory {} was deleted.'.format(directory))
            except Exception as e:
                logger.error('UnCaught exception: {}: {}'.format(type(e).__name__, e))
        time.sleep(interval)


def exit_logger(logger, app_start_time):
    """Makes ending banner for logging."""
    uptime = datetime.datetime.now() - app_start_time
    logger.info(
        '\n'
        '-------------------------------------------------------------------\n'
        '   Stopped {}\n'
        '   Uptime was {}\n'
        '-------------------------------------------------------------------\n'
        .format(__file__, str(uptime)))


def init_logger(logger, start_time):
    """Makes starting banner for logging."""

    logger.info(
        '\n'
        '-------------------------------------------------------------------\n'
        '    Running {0}\n'
        '    Started on {1}\n'
        '-------------------------------------------------------------------\n'
        .format(__file__, start_time.isoformat())
    )


def create_logger():
    """Creates logger for program."""
    logger = logging.getLogger(__file__)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s.%(msecs)03d %(name)-12s %(levelname)-8s [%(threadName)-12s] %(message)s')

    file_handler = logging.FileHandler('dirwatch.log')
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    return logger


def create_parser():
    """Creates Parser to pull in file provided."""
    parser = argparse.ArgumentParser(description='Dirwatcher Arguments')
    parser.add_argument(
        '-i', '--int',
        help='Polling interval for program.(sec) (Default=1)',
        type=int,
        default=1,
    )
    parser.add_argument(
        '-d', '--dir',
        help='Directory to search for files. (Default=./)',
        type=str,
        default='./'
    )
    parser.add_argument(
        '-t', '--text',
        help='Magic text to search for in files. (Default=magic)',
        type=str,
        default='magic'
    )
    parser.add_argument(
        '-e', '--ext',
        help='File extension of file to search through. (Default=.txt)',
        type=str,
        default='.txt'
    )
    return parser


def main():
    """Initiates the dirwatcher program."""
    parser = create_parser().parse_args()
    logger = create_logger()
    # start time
    app_start_time = datetime.datetime.now()
    # make  beginning banner
    init_logger(logger, app_start_time)
    # run dirwatcher logic
    dirwatcher(parser, logger)
    # make ending banner
    exit_logger(logger, app_start_time)


if __name__ == "__main__":
    main()
