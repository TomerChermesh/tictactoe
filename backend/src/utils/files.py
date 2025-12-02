from pathlib import Path


def create_file(file_path: str) -> None:
    path: Path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.touch()


def read_file(file_path: str) -> str | None:
    path: Path = Path(file_path)
    if not path.exists():
        return None
    
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception:
        return None


def write_to_file(file_path: str, content: str) -> bool:
    try:
        create_file(file_path)
        path: Path = Path(file_path)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    except Exception:
        return False


def append_to_file(file_path: str, content: str) -> bool:
    try:
        create_file(file_path)
        path: Path = Path(file_path)
        with open(path, 'a', encoding='utf-8') as f:
            f.write(content + '\n')
        return True
    except Exception:
        return False

