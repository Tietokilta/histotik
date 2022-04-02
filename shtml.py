import os
import re
import functools

def recurse(file):
  if os.path.isdir(file):
    for child in os.listdir(file):
      recurse(os.path.join(file, child))
  elif os.path.isfile(file) and file.endswith(".html"):
    replace_shtml(file)

def process_shtml(file, depth=0):
  # convert everything to UTF-8
  try:
    content = open(file, "r", encoding="utf-8").read()
  except UnicodeDecodeError:
    content = open(file, "r", encoding="iso-8859-1").read()

  content = re.sub(r'<!--#include\s+virtual="(.+?)"\s*-->', functools.partial(include_file, file, depth + 1), content)

  return content

def include_file(calling_file, depth, match):
  if depth > 10:
    raise RecursionError("too deeply nested #include in " + calling_file)

  resolved = os.path.join(os.path.dirname(calling_file), match.group(1))
  return process_shtml(resolved)

def replace_shtml(file, depth=0):
  content = process_shtml(file)
  open(file, "w", encoding="utf-8").write(content)

recurse(".")
