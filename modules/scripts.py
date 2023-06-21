import os.path
from modules.paths_internal import javascript_path

ScriptFile = namedTuple("ScriptFile", ['basedir', 'filename', 'path'])


# def list_scripts(dirname):
#     script_list = []
#
#     base_dir = os.path.join(javascript_path, dirname)
#
#     if os.path.exists(base_dir):
#         for filename in sorted(os.listdir(base_dir)):
#             script_list.append(ScriptFile(paths.script_path))
