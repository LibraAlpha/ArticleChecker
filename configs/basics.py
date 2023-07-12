import os

def get_root_path():
    current_dir = os.path.abspath(os.path.dirname(__file__))
    root_path = os.path.dirname(current_dir)
    return root_path


