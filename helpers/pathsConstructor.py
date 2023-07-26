# Importaciones módulos Python
import os
import sys

def pathsConstructor(relative_path):
  try:
      base_path = sys._MEIPASS
  except Exception:
      base_path = os.path.abspath(".")

  return os.path.join(base_path, relative_path)