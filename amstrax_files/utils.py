import numpy as np
import pickle
import gzip
import json
import pandas as pd
import os
import commentjson


def exporter(export_self=False):
    """
    Export utility modified from https://stackoverflow.com/a/41895194
    Returns export decorator, __all__ list
    https://github.com/AxFoundation/strax/blob/master/strax/utils.py
    """
    all_ = []
    if export_self:
        all_.append('exporter')

    def decorator(obj):
        all_.append(obj.__name__)
        return obj

    return decorator, all_


export, __all__ = exporter(export_self=True)


def read_file(path):
    """
    Open a file from disk. Auto-infers the file format
    :param path: str, file to open
    :return: opened file
    """
    # copied from straxen.common.open_resource
    # https://github.com/XENONnT/straxen/blob/a2e0e3abdbf278000cda70f7662a7d841c7223ef/straxen/common.py#L85
    name, fmt = os.path.splitext(path)

    if fmt in ['.npy', '.npy_pickle', '.npz']:
        result = np.load(path, allow_pickle=fmt == 'npy_pickle')
        if isinstance(result, np.lib.npyio.NpzFile):
            # Slurp the arrays in the file, so the result can be copied,
            # then close the file so its descriptors does not leak.
            result_slurped = {k: v[:] for k, v in result.items()}
            result.close()
            result = result_slurped
    elif fmt == '.pkl':
        with open(path, 'rb') as f:
            result = pickle.load(f)
    elif fmt == '.gz':
        subname, subfmt = os.path.splitext(name)
        if subfmt == '.pkl':
            with gzip.open(path, 'rb') as f:
                result = pickle.load(f)
        elif subfmt == '.json':
            with gzip.open(path, 'rb') as f:
                result = json.load(f)
    elif fmt == '.json':
        with open(path, mode='r') as f:
            result = commentjson.load(f)
    elif fmt == '.binary':
        with open(path, mode='rb') as f:
            result = f.read()
    elif fmt in ['.text', '.txt']:
        with open(path, mode='r') as f:
            result = f.read()
    elif fmt == '.csv':
        result = pd.read_csv(path)
    else:
        raise ValueError(f"Unsupported format {fmt}!")

    return result