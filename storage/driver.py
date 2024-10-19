from os import getcwd, path
from json import dumps, loads

STORAGE_PATH = "storage"
STORAGE_FILE = "posts.json"

FILE_PATH = path.join(getcwd(), STORAGE_PATH, STORAGE_FILE)


def read_from_file() -> list[dict]:
    with open(FILE_PATH, "r") as handle:
        return loads(handle.read())


def write_to_file(users: list[dict]):
    with open(FILE_PATH, "w") as handle:
        return handle.write(dumps(users))
