#!/usr/bin/env python3

import sys
from strike import IDFFile

# --------------------------------------------------------------------------- #

def main():

    if len(sys.argv) < 2:
        print("You need to specify a target file!")
        return

    file_path = sys.argv[1]
    idf_file = IDFFile(file_path)
    data = idf_file.process()

    for data_entry in data:
        print(f"Data: {data_entry}")

# --------------------------------------------------------------------------- #

if __name__ == '__main__':
    main()

# --------------------------------------------------------------------------- #
