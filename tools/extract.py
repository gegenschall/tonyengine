#!/usr/bin/env python
import os
from struct import unpack

FILECOUNT_OFFSET        = -4
DIRECTORY_START_OFFSET  = -8

def usage(me):
    print('Usage: %s <PCKELL.DAT> <destination>' % (me,))

def get_num_files(filename):
    with open(filename, 'rb') as f:
        # the last 4 bytes contain the number of files
        # minus one
        f.seek(FILECOUNT_OFFSET, 2)
        fcount = f.read(4)
        return int(unpack('i', fcount)[0]) + 1

def get_directory(filename):
    num_files = get_num_files(filename)
    
    with open(filename, 'rb') as f:
        # the directory start address 
        f.seek(DIRECTORY_START_OFFSET, 2)
        diroffset = int(unpack('i', f.read(4))[0])

        # seek forward to that address
        f.seek(diroffset, 0)
        
        directory = []
        for i in range(0, num_files):
            fname_len = unpack('H', f.read(2))[0] 
            fname = f.read(int(fname_len))
            offset = unpack('i', f.read(4))[0]

            entry = {}
            entry['filename'] = fname.lower()
            entry['offset'] = int(offset)
            directory.append(entry)

        directory.append({'filename' : 'DUMMY', 'offset' : diroffset})
        return directory

def extract_file(src, dest, start, size):
    print('Extracting %d bytes from offset 0x%x to %s' % (size, start, dest))
    with open(src, 'rb') as f:
        f.seek(start, 0)
        fc = f.read(size)

        with open(dest, 'wb') as out:
            out.write(fc)

def main(src, dest):
    # check if the destination exists
    if not os.path.exists(dest):
        print("Destination path does not exist")
        exit(1)

    directory = get_directory(src)
    # the last directory entry is the beginning of 
    # the directory, hence the end of a file.
    # Bit of a nasty hack. Sorry...
    for i in range(0, len(directory) - 1):
        entry = directory[i]
        entry_next = directory[i+1]

        size = entry_next['offset'] - entry['offset']
        filename = os.path.join(dest, entry['filename'])
        extract_file(src, filename, entry['offset'], size)
        
if __name__ == '__main__':
    import sys
    
    if (len(sys.argv) != 3):
        usage(sys.argv[0])
        exit(1)

    main(sys.argv[1], sys.argv[2])
