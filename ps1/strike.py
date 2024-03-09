#!/usr/bin/env python3

import struct
import sys

# =========================================================================== #

class IDFFile:
    def __init__(self, file_path):
        self.file_path    = file_path
        self.data_block   = None
        self.offset_block = None

    # ----------------------------------------------------------------------- #

    def process(self):
        with open(self.file_path, 'rb') as file:
            self.data_block   = IDFBlock(file)
            self.offset_block = IDFBlock(file)

            offsets = self.offset_block.get_offsets()
            data    = self.data_block.get_data(offsets)

            return data

        return None

# =========================================================================== #

class IDFBlock:

    # Magic bytes for each section
    SECTION_DATA    = b'\x74\x61\x44\x49'
    SECTION_OFFSETS = b'\x54\x4c\x44\x49'

    TYPE_UNKNOWN = 0
    TYPE_DATA    = 1
    TYPE_OFFSETS = 2

    # ----------------------------------------------------------------------- #

    def __init__(self, file):
        self.magic = None
        self.size = 0
        self.data = None
        self.type = 0
        self.read_block(file)

    # ----------------------------------------------------------------------- #

    def read_block(self, file):
        # Read the magic bytes (4 bytes)
        self.magic = file.read(4)
        if not self.magic:
            return  # End of file or error

        if self.magic == self.SECTION_DATA:
            self.type = self.TYPE_DATA
        if self.magic == self.SECTION_OFFSETS:
            self.type = self.TYPE_OFFSETS

        # Read the size value (4 bytes) and unpack it as an unsigned integer
        size_bytes = file.read(4)
        self.size = struct.unpack('I', size_bytes)[0]

        # Calculate the length of the sequence of bytes
        data_length = self.size - 8

        # Read the sequence of bytes
        self.data = file.read(data_length)

    # ----------------------------------------------------------------------- #

    def is_valid(self):
        # Check if the block has been successfully initialized
        return self.magic is not None and self.data is not None

    # ----------------------------------------------------------------------- #

    def get_data(self, offsets):
        if self.type != self.TYPE_DATA:
            return None

        data         = []
        offset_index = 0
        last_offset  = 0

        for offset_index in offsets:
            data_entry = self.data[last_offset:offset_index-1]
            data.append(data_entry)
            last_offset = offset_index

        return data

    # ----------------------------------------------------------------------- #

    def get_offsets(self):
        if self.type != self.TYPE_OFFSETS:
            return None

        offsets = []
        table   = self.data[12:]
        index   = 0

        while index < len(table):
            offsets.append(struct.unpack('I', table[index:index+4])[0])
            index += 8

        return offsets

    # ----------------------------------------------------------------------- #

    def __str__(self):
        return f"IDFBlock(magic={self.magic}, length={self.size})"

# =========================================================================== #
