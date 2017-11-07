from pkg_resources import resource_filename
from bob.dap.base.database import FileListPadDatabase, FileListPadFile
from bob.dap.face.database import VideoPadFile


class File(FileListPadFile, VideoPadFile):
    """The file objects of the OULU-NPU dataset."""
    pass


class Database(FileListPadDatabase):
    """The database interface for the OULU-NPU dataset."""

    def __init__(self, original_directory=None,
                 bio_file_class=None, name='oulunpu', **kwargs):
        if bio_file_class is None:
            bio_file_class = File
        filelists_directory = resource_filename(__name__, 'lists')
        super(Database, self).__init__(
            filelists_directory=filelists_directory, name=name,
            original_directory=original_directory,
            bio_file_class=bio_file_class,
            **kwargs)
