#!/usr/bin/python
# This file is part of the PySide project.
#
# Copyright (C) 2011 Nokia Corporation and/or its subsidiary(-ies).
#
# Contact: PySide team <contact@pyside.org>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# version 2 as published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA
# 02110-1301 USA

''' refashmake.py - Python-centric implementation to calculate SHA-1
    checksum of scripts. Providing ELF files may generate invalid
    signature due to BSign sections.
'''


import sys
import os
import stat
import hashlib
import logging
from optparse import OptionParser


def create_parser():
    '''Creates the option parser.

    This parser can be used by scripts/modules using refhashmake as a module
    '''
    parser = OptionParser()

    parser.add_option('-v', '--verbose', dest='verbose',
                      help='Verbose mode', action='store_true')
    parser.add_option('-f', '--file', dest='filename',
                      help='Filename as argument', action='store_true')
    parser.add_option('-b', '--no-exebit', dest='no_exebit',
                      help='Do not test execute file attribute',
                      action='store_true')
    parser.add_option('-u', '--full-path', dest='relative',
                      help='Use relative pathnames in output',
                      action='store_false')
    parser.add_option('-r', '--relative-path', dest='relative',
                      help='Use relative pathnames in output',
                      action='store_true')
    parser.add_option('-n', '--no-links', dest='no_links',
                      help='Do not generate hashes for symlinks',
                      action='store_true')
    parser.add_option('-s', '--script', dest='scripts',
                      help='Process only scripts. Default behavior.',
                      action='store_true')

    # Unsupported/unused options
    parser.add_option('-a', '--all', dest='all',
                      help='Process both script and ELF files.',
                      action='store_true')
    parser.add_option('-c', '--create', dest='newfmt',
                      help='Use new format with tag-length-value',
                      action='store_true')

    # options with values
    parser.add_option('-o', '--source-id', dest='sourceid',
                      help='Include component source identifier',
                      action='store', type='string')
    parser.add_option('-p', '--prefix', dest='prefix',
                      help='Add prefix argument to filename',
                      action='store', type='string')

    parser.set_defaults(verbose=False, filename=False, no_exebit=False,
                        relative=True, no_links=True, scripts=True,
                        sourceid='', prefix='', all=False)

    return parser


def parse_args(argv=None):
    '''Define command line arguments and parse sys.argv.'''
    if argv is None:
        argv = sys.argv

    parser = create_parser()

    return parser.parse_args(argv)


def calculate_hash(filename, algorithm=hashlib.sha1):
    '''Calculates SHA1 hex digest for a given file'''
    calc = algorithm()
    with open(filename, 'r') as handle:
        calc.update(handle.read())
        return calc.hexdigest(), calc.digest_size


def format_pathname(filename, options):
    '''Format the path given the options 'relative' and 'prefix'.'''
    length = len(filename)
    plen = len(options.prefix)
    line = ''

    if options.relative:
        offset = 1
        pstyle = 'R'
    else:
        offset = 0
        pstyle = 'F'

    if filename.startswith('./'):
        line += '%c %d %s%s' % (pstyle, length - 1 - offset + plen,
                              options.prefix, filename[1 + offset:])
    elif filename.startswith('/'):
        line += '%c %d %s%s' % (pstyle, length - offset + plen,
                              options.prefix, filename[offset:])
    else:
        line += '%c %d %s%s' % (pstyle, length + plen + 1 - offset,
                              options.prefix, filename)

    return line


def format_output(filename, digest, size, options):
    '''Returns the formatted line to be printed'''
    line = ''

    if not os.path.exists(filename):
        logging.error("Can't open file %s; exiting.", filename)
        sys.exit(1)

    # Source id. Still not used.
    if options.sourceid:
        line += 'S %d %s ' % (len(options.sourceid), options.sourceid)

    line += 'H %d %s ' % (2 * size, digest)

    line += format_pathname(filename, options)

    return line


def process_file(filename, options, stream=sys.stdout):
    '''Process a single filename print its formatted signature line.'''

    if options.no_links:
        statinfo = os.lstat(filename)
        if stat.S_ISLNK(statinfo.st_mode) or stat.S_ISDIR(statinfo.st_mode):
            return 0

    if not options.no_exebit:

        mode = stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH

        if not mode & stat.S_IMODE(statinfo.st_mode):
            return 0

        digest, size = calculate_hash(filename)
        stream.write(format_output(filename, digest, size, options) + '\n')


def main():
    '''Parse options and process files.'''
    options, args = parse_args()

    if options.verbose:
        logging.basicConfig(level=logging.DEBUG)

    # TODO Add option to read filenames from a text file.
    # Currently we just support reading files from command line
    if options.filename:
        for filename in args:
            logging.debug('Processing file: %s', filename)
            process_file(filename, options)


if __name__ == '__main__':
    main()
