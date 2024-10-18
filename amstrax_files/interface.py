import os
import pkg_resources
import amstrax_files
from amstrax_files.utils import read_file
import requests

export, __all__ = amstrax_files.exporter()

GITHUB_RAW_URL = "https://raw.githubusercontent.com/XAMS-nikhef/amstrax_files/master/corrections/"
GITHUB_RAW_URL = "https://raw.githubusercontent.com/XAMS-nikhef/amstrax_files/xams_corrections/corrections/"


@export
def list_files():
    """Get a list of files we have we have in the fax files"""
    p = _package_path("data")
    return _list_files(p)


@export
def get_file(file_name):
    """
    Get files stored under strax_files. Add "fmt = <format>" as an
    argument to read a specific format. otherwise we will assume it's in
    a text format. See straxen.get_recourse for more info.
    """
    p = _package_path("data")
    return _get_file(file_name, get_from=p)


@export
def get_correction(file_name):
    """
    Get correction file from GitHub or locally.
    It first tries to download from GitHub, and if that fails, it fetches from the local corrections directory.
    """
    # Try to get the file from GitHub
    try:
        return _fetch_from_github(file_name)
    except Exception as e:
        print(f"Failed to fetch {file_name} from GitHub: {e}")
        # Fallback to local if fetching from GitHub fails
        print(f"Falling back to local corrections for {file_name}")
        p = _package_path("corrections")
        return _get_file(file_name, get_from=p)


def _fetch_from_github(file_name):
    """Fetch correction file from GitHub raw URL"""
    url = GITHUB_RAW_URL + file_name
    response = requests.get(url)

    if response.status_code == 200:
        # Successfully fetched the file, return its contents
        print(f"Fetched {file_name} from GitHub")
        # return it as a json file (as a dictionary)
        return response.json()
    else:
        raise FileNotFoundError(f"File {file_name} not found in GitHub repository")


@export
def get_abspath(file_name, sub_dir="data"):
    """Get the abspath of the file. Raise FileNotFoundError when not found in any subfolder"""
    p = os.path.join(_package_path(sub_dir), file_name)
    if os.path.exists(p):
        return p
    raise FileNotFoundError(f"Cannot find {file_name}")


def _get_file(file_name, get_from):
    """Get a file from a subfolder in this package"""
    if file_name not in _list_files(get_from):
        raise FileNotFoundError(f"No file {file_name} in {get_from}")
    else:
        path = os.path.join(get_from, file_name)
        return read_file(path)


def _package_path(sub_directory):
    """Get the abs path of the requested sub folder"""
    return pkg_resources.resource_filename("amstrax_files", f"../{sub_directory}")


def _list_files(path):
    """List the files stored under path"""
    return os.listdir(path)
