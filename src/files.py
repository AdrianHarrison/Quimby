"""
files.py

Handles reading and writting from disk.
"""

import os
from io import BytesIO
from zipfile import ZipFile


class FileWriter():

    def write_directory(self, directory: str) -> ZipFile:
        """ Writes the contents of a directory to a zip file.

        Arguments:
            directory {str} -- Filepath of the directory to
                write into a zip.

        Returns:
            ZipFile -- The resulting ZipFile object to be
                written to disk.
        """

        zip_file = ZipFile(BytesIO(), mode="w")

        for filename in os.listdir(directory):
            with open("./%s/%s" % (directory, filename), "rb") as file:
                block = BytesIO(file.read())
                block.seek(0)
                zip_file.write(filename, block.read())

        return zip_file


class FileReader():

    def read_drectory(self):
        """ Stub """
        pass
