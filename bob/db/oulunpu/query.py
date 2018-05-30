from pkg_resources import resource_filename
from bob.pad.base.database import FileListPadDatabase
from bob.pad.face.database import VideoPadFile
from bob.extension import rc
from bob.io.video import reader
from . import OULUNPU_FRAME_SHAPE


class File(VideoPadFile):
    """The file objects of the OULU-NPU dataset."""

    @property
    def frames(self):
        """Yields the frames of the biofile one by one.

        Yields
        ------
        :any:`numpy.array`
            A frame of the video. The size is (3, 1920, 1080).
        """
        vfilename = self.make_path(
            directory=self.original_directory, extension='.avi')
        return iter(reader(vfilename))

    @property
    def number_of_frames(self):
        """Returns the number of frames in a video file.

        Returns
        -------
        int
            The number of frames.
        """
        vfilename = self.make_path(
            directory=self.original_directory, extension='.avi')
        return reader(vfilename).number_of_frames

    @property
    def frame_shape(self):
        """Returns the size of each frame in this database.

        Returns
        -------
        (int, int, int)
            The (#Channels, Height, Width) which is :any:`OULUNPU_FRAME_SHAPE`.
        """
        return OULUNPU_FRAME_SHAPE

    @property
    def annotations(self):
        """Reads the annotations

        Returns
        -------
        dict
            The annotations as a dictionary, e.g.:
            ``{'0': {'reye':(re_y,re_x), 'leye':(le_y,le_x)}, ...}``
        """
        path = self.make_path(
            directory=self.original_directory, extension='.txt')
        annotations = {}
        with open(path) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                num_frame, x_eye_left, y_eye_left, x_eye_right, y_eye_right = \
                    line.split(',')
                annotations[num_frame] = {
                    'reye': (int(y_eye_right), int(x_eye_right)),
                    'leye': (int(y_eye_left), int(x_eye_left)),
                }
        return annotations


class Database(FileListPadDatabase):
    """The database interface for the OULU-NPU dataset."""

    def __init__(self, original_directory=rc['bob.db.oulunpu.directory'],
                 name='oulunpu', pad_file_class=None,
                 original_extension=".avi", **kwargs):
        if pad_file_class is None:
            pad_file_class = File
        filelists_directory = resource_filename(__name__, 'lists')
        super(Database, self).__init__(
            filelists_directory=filelists_directory, name=name,
            original_directory=original_directory,
            pad_file_class=pad_file_class,
            original_extension=original_extension,
            training_depends_on_protocol=True,
            **kwargs)

    def objects(self, groups=None, protocol=None, purposes=None,
                model_ids=None, classes=None, **kwargs):
        files = super(Database, self).objects(
            groups=groups, protocol=protocol, purposes=purposes,
            model_ids=model_ids, classes=classes, **kwargs)
        for f in files:
            f.original_directory = self.original_directory
        return files

    def frames(self, padfile):
        return padfile.frames

    def number_of_frames(self, padfile):
        return padfile.number_of_frames

    @property
    def frame_shape(self):
        return OULUNPU_FRAME_SHAPE

    def annotations(self, padfile):
        return padfile.annotations
