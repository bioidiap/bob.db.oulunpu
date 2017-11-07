
"""OULU-NPU - a mobile face presentation attack database with real-world
variations
"""

import os
import sys
import pkg_resources
from bob.db.base.driver import Interface as BaseInterface
from bob.io.base import create_directories_safe


def dumplist(args):
    """Dumps lists of files based on your criteria"""

    from .query import Database
    db = Database()

    r = db.objects(
        purposes=args.purpose,
        groups=args.group,
    )

    output = sys.stdout
    if args.selftest:
        from bob.db.base.utils import null
        output = null()

    for f in r:
        output.write('%s\n' % f.make_path(
            directory=args.directory, extension=args.extension))

    return 0


def checkfiles(args):
    """Checks existence of files based on your criteria"""

    from .query import Database
    db = Database()

    r = db.objects()

    # go through all files, check if they are available on the filesystem
    good = []
    bad = []
    for f in r:
        if os.path.exists(f.make_path(args.directory, args.extension)):
            good.append(f)
        else:
            bad.append(f)

    # report
    output = sys.stdout
    if args.selftest:
        from bob.db.base.utils import null
        output = null()

    if bad:
        for f in bad:
            output.write('Cannot find file "%s"\n' %
                         f.make_path(args.directory, args.extension))
        output.write('%d files (out of %d) were not found at "%s"\n' %
                     (len(bad), len(r), args.directory))

    return 0


def convert_filelist_pad(path, outfolder, append, test, group):
    outfolder = os.path.join(outfolder, group)
    realpath = os.path.join(outfolder, 'for_real.lst')
    attackpath = os.path.join(outfolder, 'for_attack.lst')
    create_directories_safe(os.path.dirname(realpath))
    conv = {'1': 'real', '2': 'print1', '3': 'print2',
            '4': 'video_replay1', '5': 'video_replay2'}
    with open(path) as f, \
            open(realpath, 'w') as rf, \
            open(attackpath, 'w') as af:
        for line in f:
            if test:
                isreal = True
            if line[0] == '+':
                isreal = True
            elif line[0] == '-':
                isreal = False
            elif not test:
                print('ignoring line: ' + line)
                continue
            if test:
                filename = line.strip()
                client_id = 'test'
            else:
                _, filename = line.strip().split(',')
                _, _, client_id, attack_type = filename.split('_')
                attack_type = conv[attack_type]
            filename = append + os.sep + filename
            if isreal:
                rf.write('{} {}\n'.format(filename, client_id))
            else:
                af.write('{} {} {}\n'.format(
                    filename, client_id, attack_type))


def convert_filelist_dap(path, outfolder, append, test, group):
    if group == 'world':
        outpath = os.path.join(outfolder, 'norm', 'train_world.lst')
    else:
        outpath = os.path.join(outfolder, group, 'for_scores.lst')
        # create the empty 'for_models.lst' file.
        with open(os.path.join(outfolder, group, 'for_models.lst'), 'w') as f:
            pass
    create_directories_safe(os.path.dirname(outpath))
    conv = {'1': 'real', '2': 'print1', '3': 'print2',
            '4': 'video_replay1', '5': 'video_replay2'}
    with open(path) as f, \
            open(outpath, 'w') as wf:
        for line in f:
            if test:
                isreal = True
            if line[0] == '+':
                isreal = True
            elif line[0] == '-':
                isreal = False
            elif not test:
                print('ignoring line: ' + line)
                continue
            if test:
                filename = line.strip()
                client_id = 'test'
            else:
                _, filename = line.strip().split(',')
                _, _, client_id, attack_type = filename.split('_')
                attack_type = conv[attack_type]
            filename = os.path.join(append, filename)
            if not isreal:
                client_id = 'attack/{}/{}'.format(attack_type, client_id)

            if group == 'world':
                wf.write('{} {}\n'.format(filename, client_id))
            else:
                wf.write('{} model model {}\n'.format(filename, client_id))


def create(args):
    """Creates the file-lists to be used in Bob based on original file lists.
    """
    root_dir = args.root_dir
    output_dir = args.output_dir

    groups2 = ['world', 'dev', 'eval']
    convert_filelist = convert_filelist_dap

    for grp1, grp2 in zip(['Train', 'Dev', 'Test'],
                          groups2):
        if grp1 == 'Test':
            part = 'OULU_NPU_Part_2'
            append = 'OULU_NPU_Part_2/Files_2'
            test = True
        else:
            part = 'OULU_NPU_Part_1'
            append = 'OULU_NPU_Part_1/Files_1'
            test = False

        for protocol in ('Protocol_1', 'Protocol_2', 'Protocol_3',
                         'Protocol_4'):
            for i in range(1, 7):
                if protocol in ('Protocol_1', 'Protocol_2'):
                    textfile = '{}.txt'.format(grp1)
                    new_protocol = protocol
                else:
                    textfile = '{}_{}.txt'.format(grp1, i)
                    new_protocol = '{}_{}'.format(protocol, i)
                convert_filelist(
                    os.path.join(root_dir, part, protocol, textfile),
                    os.path.join(output_dir, new_protocol),
                    append, test, grp2)
                if protocol in ('Protocol_1', 'Protocol_2'):
                    break


class Interface(BaseInterface):

    def name(self):
        return 'oulunpu'

    def version(self):
        return pkg_resources.require('bob.db.%s' % self.name())[0].version

    def files(self):
        return ()

    def type(self):
        return 'text'

    def add_commands(self, parser):

        from . import __doc__ as docs

        subparsers = self.setup_parser(parser,
                                       "OULU-NPU database", docs)

        import argparse

        # the "dumplist" action
        parser = subparsers.add_parser('dumplist', help=dumplist.__doc__)
        parser.add_argument(
            '-d', '--directory', default='',
            help="if given, this path will be prepended to every entry "
            "returned.")
        parser.add_argument(
            '-e', '--extension', default='',
            help="if given, this extension will be appended to every entry "
            "returned.")
        parser.add_argument(
            '-u', '--purpose', help="if given, this value will limit the "
            "output files to those designed for the given purposes.",
            choices=('enroll', 'probe', ''))
        parser.add_argument(
            '-g', '--group',
            help="if given, this value will limit the output files to those "
            "belonging to a particular protocolar group.",
            choices=('dev', 'eval', 'world', ''))
        parser.add_argument('--self-test', dest="selftest",
                            action='store_true', help=argparse.SUPPRESS)
        parser.set_defaults(func=dumplist)  # action

        # the "checkfiles" action
        parser = subparsers.add_parser('checkfiles', help=checkfiles.__doc__)
        parser.add_argument(
            '-l', '--list-directory', required=True,
            help="The directory which contains the file lists.")
        parser.add_argument(
            '-d', '--directory', dest="directory", default='',
            help="if given, this path will be prepended to every entry "
            "returned.")
        parser.add_argument(
            '-e', '--extension', dest="extension", default='',
            help="if given, this extension will be appended to every entry "
            "returned.")
        parser.add_argument('--self-test', dest="selftest",
                            action='store_true', help=argparse.SUPPRESS)
        parser.set_defaults(func=checkfiles)  # action

        # the "create" action
        parser = subparsers.add_parser('create', help=create.__doc__)
        parser.add_argument(
            '-d', '--root-dir',
            help='The directory where the original database is.')
        default_output = pkg_resources.resource_filename(__name__, 'lists')
        parser.add_argument(
            '-o', '--output-dir', default=default_output,
            help='The directory where the new list files will be saved into.')
        parser.set_defaults(func=create)  # action
