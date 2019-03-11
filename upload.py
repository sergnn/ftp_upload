"""Upload files from each dir started with integer to the FTP"""
import os
import typing
from ftplib import FTP
from pathlib import Path

SRCDIR = Path('<SOURCE_DIR>')
FTP_URI = '<URL>'
FTP_CREDENTIALS = {'user': '<LOGIN>',
                   'passwd': '<PASSWORD>'}


def upload(ftp: FTP, file: Path):
    """Upload file to the FTP"""
    cwd = os.getcwd()
    os.chdir(file.parent)
    ftp.storbinary(f'STOR {file.name}', file.open('rb'), 1024)
    os.chdir(cwd)


def get_files_from_ftp(ftp: FTP) -> typing.Dict[str, int]:
    """Get size for each file on FTP"""
    files = []
    ftp.dir(files.append)
    return {file.split()[-1]: int(file.split()[4]) for file in files}


def dir_startswith_int(path: Path) -> bool:
    """Check path is dir and prefix is digit"""
    return path.is_dir() and path.stem.split('_', 1)[0].isdigit()


def matching_dirs(root: Path) -> typing.List[Path]:
    """Find all subdirs  with the name 'web'"""
    subdirs = [subdir for subdir in root.iterdir() if dir_startswith_int(subdir)]
    dirs = []
    for subdir in subdirs:
        web_dir = subdir / 'web'
        if os.path.exists(web_dir):
            dirs.append(web_dir)
    return dirs


def main():
    """Main function"""
    ftp = FTP(FTP_URI)
    ftp.login(**FTP_CREDENTIALS)
    ftp.encoding = 'utf-8'
    files_on_ftp = get_files_from_ftp(ftp)
    for subdir in matching_dirs(SRCDIR):
        for file in subdir.iterdir():
            if file.suffix == '.jpg' and not file.stem.startswith('.'):
                filesize = file.stat().st_size
                if filesize == files_on_ftp.get(file.name, -1):
                    print(f'SKIP: {file}')
                else:
                    print(f'{file} size: {filesize}')
                    upload(ftp, file)

    ftp.quit()
    print('Done')


if __name__ == '__main__':
    main()
