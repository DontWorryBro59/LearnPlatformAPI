class Config:
    db_host = 'localhost'
    db_port = '5432'
    db_name = 'psql_for_app'
    db_user = 'postgres'
    db_password = 'postgres'

    db_test_name = 'psql_for_app_test'

    @property
    def get_db_uri(self):
        return f'postgresql+asyncpg://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}'

    @property
    def get_test_db_uri(self):
        print('[LOG] Мы взяли тестовую базу данных')
        return f'postgresql+asyncpg://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_test_name}'