import os.path
import modules.paths_internal
from modules.paths_internal import javascript_path, css_path
from collections import namedtuple

ScriptFile = namedtuple("ScriptFile", ['basedir', 'filename', 'path'])


# def list_scripts(dirname):
#     script_list = []
#
#     base_dir = os.path.join(javascript_path, dirname)
#
#     if os.path.exists(base_dir):
#         for filename in sorted(os.listdir(base_dir)):
#             script_list.append(ScriptFile(paths.script_path))

def list_files_with_name(filename):
    res = []

    dirs = [javascript_path, css_path]

    for dirpath in dirs:
        if not os.path.isdir(dirpath):
            continue

        path = os.path.join(dirpath, filename)
        if os.path.isfile(path):
            res.append(path)

    return res
