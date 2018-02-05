import os
import uuid

from utils import get_optional_env, get_mandatory_env

VERSION = "0.1.2"
APP_SECRET = get_optional_env("APP_SECRET", str(uuid.uuid4()))

STORAGE_TYPE = get_optional_env("STORAGE_TYPE", "models.storage")
DATABASE_URL = get_mandatory_env("DB_URI_VAR_NAME")

ROOT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
SRC_PATH = os.path.join(ROOT_PATH, 'src')
TEST_PATH = os.path.join(ROOT_PATH, 'test')
