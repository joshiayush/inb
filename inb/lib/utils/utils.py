from typing import Any


def Type(t: Any) -> str:
  try:
    return t.__name__
  except AttributeError:
    return None


def Which(program):
  import os  # pylint: disable=import-outside-toplevel

  def is_exe(fpath):  # pylint: disable=invalid-name
    return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

  fpath, _ = os.path.split(program)
  if fpath:
    if is_exe(program):
      return program
  else:
    for path in os.environ['PATH'].split(os.pathsep):
      exe_file = os.path.join(path, program)
      if is_exe(exe_file):
        return exe_file

  return None