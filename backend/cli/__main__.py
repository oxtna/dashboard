import argparse
import sqlalchemy as sql
import sqlalchemy.orm as orm
import db
from .reset_tables import reset_tables
from .populate_database import populate_database


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="dashboard.cli",
        description="Python script for populating a database.",
    )
    parser.add_argument(
        "files",
        action="store",
        type=str,
        nargs="+",
        metavar="file",
        help="Filenames of csv files containing data following the database's schema.",
    )
    parser.add_argument(
        "-r",
        "--reset",
        action="store_true",
        help="Reset the database tables.",
    )
    args = parser.parse_args()
    files: list[str] = args.files
    reset: bool = args.reset
    engine = sql.create_engine(
        f"postgresql+psycopg2://{db.USERNAME}:{db.PASSWORD}@{db.HOST}:{db.PORT}/{db.DATABASE_NAME}"
    )
    session_factory = orm.sessionmaker(bind=engine)
    if reset:
        reset_tables(engine)
    populate_database(session_factory, files)


if __name__ == "__main__":
    main()
