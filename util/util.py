import os


def mkdir_p(path):
    """
    Equivalent to `mkdir -p`. Creates any subdirectories in path if they don't already exist.
    """
    try:
        os.makedirs(path)
    except OSError as e:
        if e.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def safe_open(path, permissions):
    """
    Open `path` for writing, creating any parent directories as needed.
    """
    mkdir_p(os.path.dirname(path))
    return open(path, permissions)
