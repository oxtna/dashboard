import fastapi
import sqlalchemy as sql
import sqlalchemy.orm as orm
import db

app = fastapi.FastAPI()
engine = sql.create_engine(
    f"postgresql+psycopg2://\
{db.USERNAME}:{db.PASSWORD}@\
{db.CONTAINER_HOST}:{db.CONTAINER_PORT}/\
{db.DATABASE_NAME}",
    pool_pre_ping=True,
)
session_factory = orm.sessionmaker(bind=engine)


@app.get("/api")
def get_schema() -> dict:
    return {}


@app.get("/api/countries")
def get_countries() -> list[dict]:
    with session_factory.begin() as session:
        country_ids = session.execute(sql.select(db.Country.id))
        country_ids = country_ids.scalars().all()
        country_ids = [
            {
                "id": country_id,
                # TODO: serializacja na JSON lub URL
                "url": "TODO",
            }
            for country_id in country_ids
        ]
    return country_ids


@app.get("/api/countries/{country_id}")
def get_country(country_id: int) -> dict | None:
    with session_factory.begin() as session:
        country_name = session.execute(
            sql.select(db.Country.name).where(db.Country.id == country_id)
        )
        country_name = country_name.scalar_one_or_none()
    if country_name is None:
        return None
    return {"id": country_id, "name": country_name}


@app.get("/api/rainfall")
def get_rainfall(
    year: int | None = None,
    country_id: int | None = None,
):
    with session_factory.begin() as session:
        statement = sql.select(
            db.Hydrosphere.country_id,
            db.Hydrosphere.year,
            db.Hydrosphere.average_rainfall,
        )
        if year:
            statement = statement.where(db.Hydrosphere.year == year)
        if country_id:
            statement = statement.where(db.Hydrosphere.country_id == country_id)
        rainfall = session.execute(statement)
        rainfall = [
            {
                "country_id": country_id,
                "year": year,
                "average_rainfall": average_rainfall,
            }
            for country_id, year, average_rainfall in rainfall.all()
        ]
    return rainfall
