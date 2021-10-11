import os

# load env variables - must already be sourced in container.
DATABASE_HOST = os.environ["DATABASE_HOST"]
POSTGRES_DB = os.environ["POSTGRES_DB"]
POSTGRES_USER = os.environ["POSTGRES_USER"]
POSTGRES_PASSWORD = os.environ["POSTGRES_PASSWORD"]

POSTGRES_CONN_STR_TEMPLATE = "postgresql://{usr}:{pw}@{host}:{port}/{dbname}"

# SQLAlchemy
SQLALCHEMY_DATABASE_URI = POSTGRES_CONN_STR_TEMPLATE.format(usr=POSTGRES_USER,
                                                            pw=POSTGRES_PASSWORD,
                                                            host=DATABASE_HOST,
                                                            port=5432,
                                                            dbname=POSTGRES_DB)

# Silence the deprecation warning
SQLALCHEMY_TRACK_MODIFICATIONS = False
