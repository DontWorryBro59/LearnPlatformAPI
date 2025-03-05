import os
from dotenv import load_dotenv


class Config:
    db_host = 'localhost'
    db_port = os.getenv('DB_PORT', '5432')
    db_name = os.getenv('DB_NAME', 'psql_for_app')
    db_user = os.getenv('DB_USER', 'postgres')
    db_password = os.getenv('DB_PASSWORD', 'postgres')
    db_test_name = os.getenv('DB_TEST_NAME', 'psql_for_app_test')

    @property
    def get_db_uri(self):
        url = f'postgresql+asyncpg://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}'
        print(url)
        return url

    @property
    def get_test_db_uri(self):
        url = f'postgresql+asyncpg://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_test_name}'
        print(url)
        return url