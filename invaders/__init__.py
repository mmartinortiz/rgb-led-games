import os
import pathlib

BASEPATH = pathlib.Path(__file__).parent.resolve()
ASSETS = os.path.join(BASEPATH, "assets")


def get_asset(f: str) -> str:
    """Returns the absolute path of the file "f" to the assets folder"""
    return os.path.join(ASSETS, f)
