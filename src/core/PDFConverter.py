import pdf2image, os, sys
from pathlib import Path

poppler_path = os.path.join(Path().absolute(),'vendor','poppler','bin')
env = os.environ.copy()

if env.get("LD_LIBRARY_PATH") is None:
    os.environ["PATH"] = poppler_path
    sys.path.append(poppler_path)

print(env.get("LD_LIBRARY_PATH"))
