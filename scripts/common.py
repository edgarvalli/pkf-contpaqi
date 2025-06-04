import sys
from pathlib import Path

def set_root_path() -> str:
    root_path: Path = Path(__file__).absolute().parent.parent
    sys.path.append(str(root_path))
    return root_path