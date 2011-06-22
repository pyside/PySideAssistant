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

''' deb-add - Python port of the Perl script with a similar name that
adds/replaces files in binary debian packages.'''

import sys
import os
import re
import logging
import stat
from optparse import OptionParser

def parse_args():
    '''Parse command line options from sys.argv'''
    parser = OptionParser()

    parser.add_option('-c', '--control', dest='control',
                      help='Control file for reading.',
                      action='store', type='string')

    parser.set_defaults(control='', verbose=False)

    return parser.parse_args()

def parse_control(control):
    '''Get name, version and arch from a debian control file'''
    name, version, arch = '', '', ''
    namere = re.compile('^Package:\s*(\S+)\s*$')
    versionre = re.compile('^Version:\s*(\S+)\s*$')
    archre = re.compile('^Architecture:\s*(\S+)\s*$')
    with open(control) as handle:
        for line in handle:
            match = namere.search(line)
            if match:
                name = match.groups()[0]
                continue
            match = versionre.search(line)
            if match:
                version = match.groups()[0]
                continue
            match = archre.search(line)
            if match:
                arch = match.groups()[0]
                continue

    logging.debug('Found name %s, version %s, arch %s', (name, version, arch))
    if not all([name, version, arch]):
        logging.critical("Couldn't parse control file %s", control)
        sys.exit(1)

    return name, version, arch


def replace_files(newdeb, debfile, changes, control):
    '''Replace or copy the existing files in the debian archive'''
    name = control[0]
    to_remove = []

    with open(debfile, 'rb') as deb:

        # magic:
        magic = '!<arch>\n'
        debmagic = deb.read(8)

        if debmagic != magic:
            logging.critical("File %s does not have .deb magic number", debfile)
            sys.exit(1)

        newdeb.write(magic)

        # ar_name[16];    +00
        # ar_date[12];    +16 (= seconds since)
        # ar_uid[6]       +28 (= "0     ")
        # ar_gid[6]       +34 (= "0     ")
        # ar_mode[8]      +40 (= "100644  ")
        # ar_size[10];    +48
        # ar_fmag[2];     +58 (= "`\n")
        # -------------------
        #                 =60

        # List existing files that could be replaced.
        while 1:
            header = deb.read(60)
            if len(header) <= 0:
                break
            member = header[:16]
            size = int(header[48:58])
            if size & 1:
                size += 1

            if header[58:60] != '`\n':
                logging.warning('Bad AR header.')
                break # We're done with the existing files.

            # Should we replace it?
            if member.strip() in changes:
                source, mtime, newsize, target = changes[member.strip()]
                to_remove.append(member.strip())

                print 'Replacing', member

                header = header[:16] + '%-12s' % mtime + header[16+12:]
                header = header[:48] + '%-10s' % newsize + header[48+10:]
                newdeb.write(header)
                with open(source, 'rb') as temp:
                    buf = temp.read(newsize)
                    if len(buf) != newsize:
                        logging.critical('Failed to read %s fully', source)
                        sys.exit(0)
                    newdeb.write(buf)
                if newsize & 1:
                    newdeb.write('\n')

            newdeb.write(header)
            newdeb.write(deb.read(size))

    # Update files dict to avoid files being added again.
    for name in to_remove:
        del changes[name]


def add_files(newdeb, files):
    '''Add new files to the debian archive.'''

    for name, info in files.items():
        print 'Inserting', name
        if not info[3]:
            continue
        newsize = info[2]
        newhdr = "%-16s%-12s%-6s%-6s%-8s%-10s`\n"
        newhdr %= (info[3],
                        info[1],
                        '0',
                        '0',
                        '100644',
                        info[2])

        newdeb.write(newhdr)
        with open(info[0], 'rb') as temp:
            buf = temp.read(newsize)
            if len(buf) != newsize:
                logging.critical('Failed to read %s fully', info[0])
                sys.exit(1)
            newdeb.write(buf)
        if newsize & 1:
            newdeb.write('\n')

def process_args(args):
    '''Process the arguments with the file pairs
    Return a dict of tuples.

    Key: target file in the deb archive
    Values: (source file, last modification time, size in bytes, target file.
    '''

    files = {}

    for arg in args:
        try:
            source, target = arg.split('=')
        except ValueError:
            logging.critical('Filenames must be <source>=<target>')
            sys.exit(1)

        if not (os.path.exists(source) and os.path.isfile(source)):
            logging.critical('Source file must be a regular file')
            sys.exit(1)

        if len(target) > 16:
            logging.critical('Target file must be at most 16 characters')
            sys.exit(1)

        st = os.stat(source)

        files[target] = (source, st[stat.ST_MTIME], st[stat.ST_SIZE], target)

    return files


def main():

    options, args = parse_args()

    if options.verbose:
        logging.basicConfig(level=logging.DEBUG)

    if options.control:
        # try to parse the provided control file
        name, version, arch = parse_control(options.control)

        control = name, version, arch
        debfile = '%s_%s_%s.deb' % (name, version, arch)
    else:
        if not args:
            logging.critical('Must provide a control or debian file.')
            sys.exit(1)
        debfile = args[0]

    files = process_args(args)

    if not files:
        logging.warning('No files to be injected. Exiting')
        sys.exit(0)

    with open(debfile+'.new', 'wb') as newdeb:

        replace_files(newdeb, debfile, files, control)

        add_files(newdeb, files)

    os.rename(debfile+'.new', debfile)


if __name__ == '__main__':
    main()
