
'''Helper module to deal with arfiles (e.g. deb files)'''

import os
import sys


def is_arfile(archive):
    with open(archive, 'rb') as handle:
        return handle.read(8) == "!<arch>\n"


def get_members(archive):
    '''Gets a list of all members of this archive'''

    if not is_arfile(archive):
        return []

    members = []

    with open(archive, 'rb') as handle:
        handle.read(8)

        while True:
            header = handle.read(60)
            if not header.strip():
                break
            filename = header[:16].strip()
            if filename.endswith('/'): # Strip GNU extensions
                filename = filename[:-1]
            members.append(filename)
            filesize = int(header[48:58])
            handle.seek(filesize, os.SEEK_CUR)

    return members


def extract(archive, name=None, targetdir=None):
    '''Extract all files or just 'name' from 'archive' into targetdir'''

    if targetdir is None:
        targetdir = os.curdir

    if not is_arfile(archive):
        raise ValueError('Not an ar file')

    with open(archive, 'rb') as handle:
        handle.read(8)

        while True:
            header = handle.read(60)
            if not header.strip():
                break

            filename = header[:16].strip()
            if filename.endswith('/'):
                filename = filename[:-1]

            filesize = int(header[48:58])

            if not name or filename == name:
                with open(os.path.join(targetdir, filename), 'wb') as output:
                    filedata = handle.read(filesize)
                    output.write(filedata)
                    if filesize % 2:
                        handle.read(1)
                    #TODO handle permissions?
                if name:
                    break
            else:
                if filesize % 2:
                    filesize += 1
                handle.seek(filesize, os.SEEK_CUR)


if __name__ == '__main__':
    name = sys.argv[1]
    print is_arfile(name)

    print get_members(name)

    extract(name)

