class PostgresDB:
    def __init__(self, dbname, user, password, host="localhost", port=5432):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.connection = None

    def connect(self):
        import psycopg2

        try:
            self.connection = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
            )
            print("Connection to PostgreSQL established.")
        except Exception as e:
            print(f"Error connecting to PostgreSQL: {e}")

    def execute_query(self, query, params=None):
        if self.connection is None:
            print("Connection is not established. Call connect() first.")
            return None
        cursor = self.connection.cursor()
        try:
            cursor.execute(query, params)
            self.connection.commit()
            # Only fetch results for SELECT queries otherwise there is an error
            # when trying to fetch results from an INSERT/UPDATE/DELETE query
            if query.strip().lower().startswith("select"):
                return cursor.fetchall()
            return None  # For INSERT/UPDATE/DELETE queries
        except Exception as e:
            print(f"Error executing query: {e}")
            self.connection.rollback()
        finally:
            cursor.close()

    def close(self):
        if self.connection:
            self.connection.close()
            print("PostgreSQL connection closed.")
