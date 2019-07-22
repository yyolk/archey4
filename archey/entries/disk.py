"""Disk usage detection class"""

from subprocess import check_output

from archey.constants import COLOR_DICT


class Disk:
    """Uses `df` command output to compute the total disk usage across devices"""
    def __init__(self):
        # This dictionary will store values obtained from sub-processes calls.
        self.usage = {
            'used': 0,
            'total': 0
        }

        self._run_df_usage()

        percentage = (self.usage['used'] / self.usage['total']) * 100

        self.value = '{0}{1} GB{2} / {3} GB'.format(
            COLOR_DICT['sensors'][int(percentage // 33.34)],
            self.usage['used'],
            COLOR_DICT['clear'],
            self.usage['total']
        )

    def _run_df_usage(self):
        df_output = check_output(
            [
                'df', '-l', '-B', 'GB', '--total',
                '-t', 'ext4', '-t', 'ext3', '-t', 'ext2',
                '-t', 'reiserfs', '-t', 'jfs', '-t', 'zfs',
                '-t', 'ntfs', '-t', 'fat32', '-t', 'fuseblk',
                '-t', 'xfs', '-t', 'simfs', '-t', 'lxfs'
            ],
            env={'LANG': 'C'}, universal_newlines=True
        ).splitlines()[-1].split()

        self.usage['used'] += int(df_output[2].rstrip('GB'))
        self.usage['total'] += int(df_output[1].rstrip('GB'))
