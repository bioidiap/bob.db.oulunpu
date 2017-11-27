from pkg_resources import resource_filename
from bob.pad.base.database import FileListPadDatabase
from bob.pad.face.database import VideoPadFile
from bob.pad.face.utils import frames, number_of_frames
# documentation imports
import numpy


class File(VideoPadFile):
    """The file objects of the OULU-NPU dataset."""
    pass


class Database(FileListPadDatabase):
    """The database interface for the OULU-NPU dataset."""

    def __init__(self, original_directory=None,
                 name='oulunpu', bio_file_class=None,
                 original_extension=".avi", **kwargs):
        if bio_file_class is None:
            bio_file_class = File
        filelists_directory = resource_filename(__name__, 'lists')
        super(Database, self).__init__(
            filelists_directory=filelists_directory, name=name,
            original_directory=original_directory,
            bio_file_class=bio_file_class,
            original_extension=original_extension,
            **kwargs)

    def frames(self, padfile):
        """Yields the frames of the padfile one by one.

        Parameters
        ----------
        padfile : :any:`File`
            The high-level pad file

        Yields
        ------
        :any:`numpy.array`
            A frame of the video. The size is (3, 1920, 1080).
        """
        vfilename = padfile.make_path(
            directory=self.original_directory,
            extension=self.original_extension)
        for retval in frames(vfilename):
            yield retval

    def number_of_frames(self, padfile):
        """Returns the number of frames in a video file.

        Parameters
        ----------
        padfile : :any:`File`
            The high-level pad file

        Returns
        -------
        int
            The number of frames.
        """
        vfilename = padfile.make_path(
            directory=self.original_directory,
            extension=self.original_extension)
        return number_of_frames(vfilename)

    @property
    def frame_shape(self):
        """Returns the size of each frame in this database.

        Returns
        -------
        (int, int, int)
            The (#Channels, Height, Width) which is (3, 1920, 1080).
        """
        return (3, 1920, 1080)
