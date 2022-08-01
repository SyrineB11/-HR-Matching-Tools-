import sqlalchemy
from source.db_helpers.db_connection import metadata, engine
resumes = sqlalchemy.Table(
    "resumes",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("filename", sqlalchemy.String),
    sqlalchemy.Column("filepath", sqlalchemy.String),
)
metadata.create_all(engine)
