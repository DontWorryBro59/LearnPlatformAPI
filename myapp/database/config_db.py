class Config:
    db_host = 'localhost'
    db_port = '5432'
    db_name = 'psql_for_app'
    db_user = 'postgres'
    db_password = '11223344Qq'

    db_test_host = 'localhost'
    db_test_port = '5433'
    db_test_name = 'psql_for_app_test'
    db_test_user = 'postgres_test'
    db_test_password = 'postgres_test'

    @property
    def get_db_uri(self):
        return f'postgresql+asyncpg://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}'

    @property
    def get_test_db_uri(self):
        return f'postgresql+asyncpg://{self.db_test_user}:{self.db_test_password}@{self.db_test_host}:{self.db_test_port}/{self.db_test_name}'