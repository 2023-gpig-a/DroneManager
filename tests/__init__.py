import os
import sys

# from https://docs.python-guide.org/writing/structure/#test-suite
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from . import test_area_resolution
