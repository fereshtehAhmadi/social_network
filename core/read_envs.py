import os
from pathlib import Path

from environ.environ import Env

env = Env()
project_path = Path(__file__).resolve().parent.parent
env.read_env(str(project_path / ".env"))


def read_from_envs():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", f"core.settings")

    if env.bool("USE_DOCKER", default=False) is False:
        envs_folder = project_path / f".envs/"
        for file_path in envs_folder.glob(".*"):
            env.read_env(str(file_path))

    db_host = (
        "localhost"
        if env.bool("USE_DOCKER", default=False) is False
        else env("POSTGRES_HOST")
    )
    os.environ.setdefault(
        "DATABASE_URL",
        f"postgres://{env('POSTGRES_USER')}:{env('POSTGRES_PASSWORD')}@{db_host}:{env('POSTGRES_PORT')}/{env('POSTGRES_DB')}",
    )
    return env
