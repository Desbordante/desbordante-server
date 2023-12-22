from sqlalchemy import create_engine
from app.settings import get_settings


test_settings = get_settings()
test_settings.postgres_db = "desbordante-test"

test_engine = create_engine(test_settings.postgres_dsn.unicode_string())
