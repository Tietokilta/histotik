import os
import shutil
import re
import functools

def recurse(file, outfile):
  if os.path.isdir(file):
    os.mkdir(outfile)
    for child in os.listdir(file):
      # ignore build-related stuff
      if file == "." and child in ("build", ".git", ".gitignore", ".github", "shtml.py", "cgi-bin"):
        continue
      recurse(os.path.join(file, child), os.path.join(outfile, child))
  elif os.path.isfile(file) and file.endswith(".html"):
    replace_shtml(file, outfile)
  elif os.path.isfile(file):
    shutil.copy(file, outfile)

def process_shtml(file, depth=0):
  # convert everything to UTF-8
  try:
    content = open(file, "r", encoding="utf-8").read()
  except UnicodeDecodeError:
    content = open(file, "r", encoding="iso-8859-1").read()

  content = re.sub(r'<!--#include\s+virtual="(.+?)"\s*-->', functools.partial(include_file, file, depth + 1), content)

  content = re.sub(r'<head>', r'\g<0>\n<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />', content, 1, re.IGNORECASE)

  return content

def include_file(calling_file, depth, match):
  if depth > 10:
    raise RecursionError("too deeply nested #include in " + calling_file)

  resolved = os.path.join(os.path.dirname(calling_file), match.group(1))
  return process_shtml(resolved, depth)

def replace_shtml(file, outfile):
  content = process_shtml(file)
  open(outfile, "w", encoding="utf-8").write(content)

if os.path.exists("build"):
  shutil.rmtree("build")

recurse(".", "build")
