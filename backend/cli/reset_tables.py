import sqlalchemy as sql
import db


def reset_tables(engine: sql.Engine) -> None:
    metadata = sql.MetaData()
    metadata.reflect(bind=engine)
    metadata.drop_all(bind=engine)
    db.Base.metadata.create_all(bind=engine)
