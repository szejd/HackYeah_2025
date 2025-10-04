"""Database connection string builder utilities."""

from app.config import DBType


class ConnectionStringBuilder:
    """Builder for creating database connection strings for SQLite or PostgreSQL."""

    @staticmethod
    def build_sqlite(db_name: str) -> str:
        """
        Build a SQLite connection string.

        Args:
            db_name: The name/path of the SQLite database file or ':memory:' for in-memory database

        Returns:
            SQLite connection string

        Example:
            >>> ConnectionStringBuilder.build_sqlite('example.db')
            'sqlite:///example.db'
            >>> ConnectionStringBuilder.build_sqlite(':memory:')
            'sqlite:///:memory:'
        """
        return f"sqlite:///{db_name}"

    @staticmethod
    def build_postgresql(
        db_name: str,
        username: str,
        password: str,
        host: str = "localhost",
        port: int = 5432,
    ) -> str:
        """
        Build a PostgreSQL connection string.

        Args:
            db_name: The name of the PostgreSQL database
            username: Database username
            password: Database password
            host: Database host (default: localhost)
            port: Database port (default: 5432)

        Returns:
            PostgreSQL connection string

        Example:
            >>> ConnectionStringBuilder.build_postgresql(
            ...     db_name="mydb",
            ...     username="user",
            ...     password="pass"
            ... )
            'postgresql://user:pass@localhost:5432/mydb'
        """
        return f"postgresql://{username}:{password}@{host}:{port}/{db_name}"

    @classmethod
    def build(
        cls,
        db_type: DBType,
        db_name: str,
        username: str | None = None,
        password: str | None = None,
        host: str = "localhost",
        port: int = 5432,
    ) -> str:
        """
        Build a connection string based on database type.

        Args:
            db_type: Type of database (DBType.SQLITE or DBType.POSTGRESQL)
            db_name: The name of the database
            username: Database username (required for PostgreSQL)
            password: Database password (required for PostgreSQL)
            host: Database host (default: localhost, PostgreSQL only)
            port: Database port (default: 5432, PostgreSQL only)

        Returns:
            Database connection string

        Raises:
            ValueError: If db_type is not supported or required parameters are missing

        Example:
            >>> ConnectionStringBuilder.build(DBType.SQLITE, 'example.db')
            'sqlite:///example.db'
            >>> ConnectionStringBuilder.build(
            ...     DBType.POSTGRESQL,
            ...     'mydb',
            ...     username='user',
            ...     password='pass'
            ... )
            'postgresql://user:pass@localhost:5432/mydb'
        """
        if db_type == DBType.SQLITE:
            return cls.build_sqlite(db_name)
        elif db_type == DBType.POSTGRESQL:
            if not username or not password:
                raise ValueError("PostgreSQL requires username and password")
            return cls.build_postgresql(db_name, username, password, host, port)
        else:
            raise ValueError(
                f"Unsupported database type: {db_type}. Supported types: {DBType.SQLITE}, {DBType.POSTGRESQL}"
            )
