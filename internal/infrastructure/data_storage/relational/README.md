# relational module
The relational module contains the tools for interacting with relational databases using SQLAlchemy. It is designed to be modular, allowing for easy extension to different database systems. Currently, the focus is on the PostgreSQL database, but this can be extended to other systems if needed.
## Structure
`model` - this submodule defines the database models used by the application. These models are mapped to relational database tables using SQLAlchemy ORM.

`postgres` - this submodule contains tools for working with postgres, such as session provided by SQLAlchemy, migrations provided by alembic, and so on.

## Extensibility
The `relational` module is designed to support different **relational** databases(supported by SQLAlchemy). If you need to integrate with a different database system, you can create a new submodule within relational (e.g., `MySQL` or `SQLite`) and implement the necessary logic for that database while maintaining the same structure as the Postgres submodule.
