from pkg_resources import resource_filename
from bob.dap.base.database import FileListPadDatabase, FileListPadFile
from bob.dap.face.database import VideoPadFile
from bob.dap.face.utils import frames
# documentation imports
import numpy


class File(FileListPadFile, VideoPadFile):
    """The file objects of the OULU-NPU dataset."""
    pass


class Database(FileListPadDatabase):
    """The database interface for the OULU-NPU dataset."""

    def __init__(self, original_directory=None,
                 bio_file_class=None, name='oulunpu',
                 original_extension=".avi", **kwargs):
        if bio_file_class is None:
            bio_file_class = File
        filelists_directory = resource_filename(__name__, 'lists')
        super(Database, self).__init__(
            filelists_directory=filelists_directory, name=name,
            original_directory=original_directory,
            bio_file_class=bio_file_class,
            original_extension=original_extension,
            training_depends_on_protocol=True,
            models_depend_on_protocol=True,
            **kwargs)

    def frames(self, padfile):
        """Yields the number of frames and then the frames of the padfile one
        by one.

        Parameters
        ----------
        padfile : :any:`File`
            The high-level replay pad file
        dir : str
            The directory where the original data is.
        ext : str
            The original extension of the video files.

        Yields
        ------
        int
            The number of frames. Then, it yields the frames.
        :any:`numpy.array`
            A frame of the video. The size is (3, 1920, 1080).
        """
        vfilename = padfile.make_path(
            directory=self.original_directory,
            extension=self.original_extension)
        for retval in frames(vfilename):
            yield retval

    def frame_size(self):
        return (3, 1920, 1080)
