import os
import pkg_resources
import amstrax_files
from amstrax_files.utils import read_file

export, __all__ = amstrax_files.exporter()


@export
def list_files():
    """Get a list of files we have we have in the fax files"""
    p = _package_path('data')
    return _list_files(p)


@export
def get_file(file_name):
    """
    Get files stored under strax_files. Add "fmt = <format>" as an
    argument to read a specific format. otherwise we will assume it's in
    a text format. See straxen.get_recourse for more info.
    """
    p = _package_path('data')
    return _get_file(file_name, get_from=p)


@export
def get_abspath(file_name, sub_dir='data'):
    """Get the abspath of the file. Raise FileNotFoundError when not found in any subfolder"""
    p = os.path.join(_package_path(sub_dir), file_name)
    if os.path.exists(p):
        return p
    raise FileNotFoundError(f'Cannot find {file_name}')


def _get_file(file_name, get_from):
    """Get a file from a subfolder in this package"""
    if file_name not in _list_files(get_from):
        raise FileNotFoundError(f'No file {file_name} in {get_from}')
    else:
        path = os.path.join(get_from, file_name)
        return read_file(path)


def _package_path(sub_directory):
    """Get the abs path of the requested sub folder"""
    return pkg_resources.resource_filename('amstrax_files', f'../{sub_directory}')


def _list_files(path):
    """List the files stored under path"""
    return os.listdir(path)
