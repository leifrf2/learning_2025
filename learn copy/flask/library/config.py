from flask_sqlalchemy import SQLAlchemy

db: SQLAlchemy = SQLAlchemy()
sqlite_db_name = 'sqlite:///books.db'
