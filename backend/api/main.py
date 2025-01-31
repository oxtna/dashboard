from fastapi import FastAPI
import uvicorn
import sqlalchemy as sql
import sqlalchemy.orm as orm
import db

app = FastAPI(title="Dashboard API", root_path="/api/v1")
engine = sql.create_engine(
    f"postgresql+psycopg2://\
{db.USERNAME}:{db.PASSWORD}@\
{db.CONTAINER_HOST}:{db.CONTAINER_PORT}/\
{db.DATABASE_NAME}",
    pool_pre_ping=True,
)
session_factory = orm.sessionmaker(bind=engine)


@app.get("/countries")
def get_countries():
    with session_factory.begin() as session:
        statement = sql.select(db.Country.id)
        countries = session.execute(statement)
        countries = countries.scalars().all()
        countries = [{"id": country_id, "url": "TODO"} for country_id in countries]
        return countries


@app.get("/countries/{country_id}")
def get_country(country_id: int):
    with session_factory.begin() as session:
        statement = sql.select(db.Country).where(db.Country.id == country_id)
        country = session.execute(statement)
        country = country.scalar_one_or_none()
        if country is None:
            return None
        return {
            "id": country.id,
            "name": country.name,
        }


@app.get("/temperatures")
def get_temperatures(
    country: int | None = None,
    year: int | None = None,
):
    with session_factory.begin() as session:
        statement = sql.select(
            db.Temperature.country_id,
            db.Temperature.year,
            db.Temperature.average_temperature,
            db.Temperature.temperature_anomaly,
        )
        if country is not None:
            statement = statement.where(db.Temperature.country_id == country)
        if year is not None:
            statement = statement.where(db.Temperature.year == year)
        temperatures = session.execute(statement)
        temperatures = [
            {
                "country": country_id,
                "year": year_,
                "average_temperature": average_temperature,
                "temperature_anomaly": temperature_anomaly,
            }
            for country_id, year_, average_temperature, temperature_anomaly in temperatures
        ]
        return temperatures


@app.get("/temperatures/average")
def get_average_temperatures(
    country: int | None = None,
    year: int | None = None,
):
    with session_factory.begin() as session:
        statement = sql.select(
            db.Temperature.country_id,
            db.Temperature.year,
            db.Temperature.average_temperature,
        )
        if country is not None:
            statement = statement.where(db.Temperature.country_id == country)
        if year is not None:
            statement = statement.where(db.Temperature.year == year)
        average_temperatures = session.execute(statement)
        average_temperatures = [
            {
                "country": country_id,
                "year": year_,
                "average_temperature": average_temperature,
            }
            for country_id, year_, average_temperature in average_temperatures
        ]
        return average_temperatures


@app.get("/temperatures/anomaly")
def get_temperature_anomalies(
    country: int | None = None,
    year: int | None = None,
):
    with session_factory.begin() as session:
        statement = sql.select(
            db.Temperature.country_id,
            db.Temperature.year,
            db.Temperature.temperature_anomaly,
        )
        if country is not None:
            statement = statement.where(db.Temperature.country_id == country)
        if year is not None:
            statement = statement.where(db.Temperature.year == year)
        temperature_anomalies = session.execute(statement)
        temperature_anomalies = [
            {
                "country": country_id,
                "year": year_,
                "temperature_anomaly": temperature_anomaly,
            }
            for country_id, year_, temperature_anomaly in temperature_anomalies
        ]
        return temperature_anomalies


@app.get("/population")
def get_population(
    country: int | None = None,
    year: int | None = None,
):
    with session_factory.begin() as session:
        statement = sql.select(
            db.Population.country_id,
            db.Population.year,
            db.Population.population,
        )
        if country is not None:
            statement = statement.where(db.Population.country_id == country)
        if year is not None:
            statement = statement.where(db.Population.year == year)
        population = session.execute(statement)
        population = [
            {"country": country_id, "year": year_, "population": population_}
            for country_id, year_, population_ in population
        ]
        return population


@app.get("/gdp")
def get_gdp(
    country: int | None = None,
    year: int | None = None,
):
    with session_factory.begin() as session:
        statement = sql.select(
            db.Population.country_id,
            db.Population.year,
            db.Population.gdp,
        )
        if country is not None:
            statement = statement.where(db.Population.country_id == country)
        if year is not None:
            statement = statement.where(db.Population.year == year)
        gdp = session.execute(statement)
        gdp = [
            {"country": country_id, "year": year_, "gdp": gdp_}
            for country_id, year_, gdp_ in gdp
        ]
        return gdp


@app.get("/pollution")
def get_pollution(
    country: int | None = None,
    year: int | None = None,
):
    with session_factory.begin() as session:
        statement = sql.select(
            db.Pollution.country_id,
            db.Pollution.year,
            db.Pollution.co2_emissions,
            db.Pollution.methane_emissions,
            db.Pollution.air_pollution_index,
            db.Pollution.ocean_acidification,
            db.Pollution.per_capita_emissions,
        )
        if country is not None:
            statement = statement.where(db.Pollution.country_id == country)
        if year is not None:
            statement = statement.where(db.Pollution.year == year)
        pollution = session.execute(statement)
        pollution = [
            {
                "country": country_id,
                "year": year_,
                "co2": co2_emissions,
                "methane": methane_emissions,
                "air_pollution_index": air_pollution_index,
                "ocean_acidification": ocean_acidification,
                "per_capita_emissions": per_capita_emissions,
            }
            for (
                country_id,
                year_,
                co2_emissions,
                methane_emissions,
                air_pollution_index,
                ocean_acidification,
                per_capita_emissions,
            ) in pollution
        ]
        return pollution


@app.get("/pollution/co2")
def get_co2_emissions(
    country: int | None = None,
    year: int | None = None,
):
    with session_factory.begin() as session:
        statement = sql.select(
            db.Pollution.country_id,
            db.Pollution.year,
            db.Pollution.co2_emissions,
        )
        if country is not None:
            statement = statement.where(db.Pollution.country_id == country)
        if year is not None:
            statement = statement.where(db.Pollution.year == year)
        co2_emissions = session.execute(statement)
        co2_emissions = [
            {
                "country": country_id,
                "year": year_,
                "co2_emissions": co2_emissions_,
            }
            for country_id, year_, co2_emissions_ in co2_emissions
        ]
        return co2_emissions


@app.get("/pollution/methane")
def get_methane_emissions(
    country: int | None = None,
    year: int | None = None,
):
    with session_factory.begin() as session:
        statement = sql.select(
            db.Pollution.country_id,
            db.Pollution.year,
            db.Pollution.methane_emissions,
        )
        if country is not None:
            statement = statement.where(db.Pollution.country_id == country)
        if year is not None:
            statement = statement.where(db.Pollution.year == year)
        methane_emissions = session.execute(statement)
        methane_emissions = [
            {
                "country": country_id,
                "year": year_,
                "methane_emissions": methane_emissions_,
            }
            for country_id, year_, methane_emissions_ in methane_emissions
        ]
        return methane_emissions


@app.get("/pollution/air-pollution-index")
def get_air_pollution_index(
    country: int | None = None,
    year: int | None = None,
):
    with session_factory.begin() as session:
        statement = sql.select(
            db.Pollution.country_id,
            db.Pollution.year,
            db.Pollution.air_pollution_index,
        )
        if country is not None:
            statement = statement.where(db.Pollution.country_id == country)
        if year is not None:
            statement = statement.where(db.Pollution.year == year)
        air_pollution_index = session.execute(statement)
        air_pollution_index = [
            {
                "country": country_id,
                "year": year_,
                "air_pollution_index": air_pollution_index_,
            }
            for country_id, year_, air_pollution_index_ in air_pollution_index
        ]
        return air_pollution_index


@app.get("/pollution/ocean-acidification")
def get_ocean_acidification(
    country: int | None = None,
    year: int | None = None,
):
    with session_factory.begin() as session:
        statement = sql.select(
            db.Pollution.country_id,
            db.Pollution.year,
            db.Pollution.ocean_acidification,
        )
        if country is not None:
            statement = statement.where(db.Pollution.country_id == country)
        if year is not None:
            statement = statement.where(db.Pollution.year == year)
        ocean_acidification = session.execute(statement)
        ocean_acidification = [
            {
                "country": country_id,
                "year": year_,
                "ocean_acidification": ocean_acidification_,
            }
            for country_id, year_, ocean_acidification_ in ocean_acidification
        ]
        return ocean_acidification


@app.get("/pollution/per-capita")
def get_per_capita_emissions(
    country: int | None = None,
    year: int | None = None,
):
    with session_factory.begin() as session:
        statement = sql.select(
            db.Pollution.country_id,
            db.Pollution.year,
            db.Pollution.per_capita_emissions,
        )
        if country is not None:
            statement = statement.where(db.Pollution.country_id == country)
        if year is not None:
            statement = statement.where(db.Pollution.year == year)
        per_capita_emissions = session.execute(statement)
        per_capita_emissions = [
            {
                "country": country_id,
                "year": year_,
                "per_capita_emissions": per_capita_emissions_,
            }
            for country_id, year_, per_capita_emissions_ in per_capita_emissions
        ]
        return per_capita_emissions


@app.get("/energy")
def get_energy(
    country: int | None = None,
    year: int | None = None,
):
    with session_factory.begin() as session:
        statement = sql.select(
            db.Energy.country_id,
            db.Energy.year,
            db.Energy.renewable_energy_usage,
            db.Energy.solar_energy_potential,
            db.Energy.fossil_fuel_usage,
            db.Energy.energy_consumption_per_capita,
        )
        if country is not None:
            statement = statement.where(db.Energy.country_id == country)
        if year is not None:
            statement = statement.where(db.Energy.year == year)
        energy = session.execute(statement)
        energy = [
            {
                "country": country_id,
                "year": year_,
                "renewable_energy_usage": renewable_energy_usage,
                "solar_energy_potential": solar_energy_potential,
                "fossil_fuel_usage": fossil_fuel_usage,
                "energy_consumption_per_capita": energy_consumption_per_capita,
            }
            for (
                country_id,
                year_,
                renewable_energy_usage,
                solar_energy_potential,
                fossil_fuel_usage,
                energy_consumption_per_capita,
            ) in energy
        ]
        return energy


@app.get("/hydrosphere")
def get_hydrosphere(
    country: int | None = None,
    year: int | None = None,
):
    with session_factory.begin() as session:
        statement = sql.select(
            db.Hydrosphere.country_id,
            db.Hydrosphere.year,
            db.Hydrosphere.sea_level_rise,
            db.Hydrosphere.arctic_ice_extent,
            db.Hydrosphere.average_rainfall,
        )
        if country is not None:
            statement = statement.where()
        if year is not None:
            statement = statement.where()
        hydrosphere = session.execute(statement)
        hydrosphere = [
            {
                "country": country_id,
                "year": year_,
                "sea_level_rise": sea_level_rise,
                "arctic_ice_extent": arctic_ice_extent,
                "average_rainfall": average_rainfall,
            }
            for (
                country_id,
                year_,
                sea_level_rise,
                arctic_ice_extent,
                average_rainfall,
            ) in hydrosphere
        ]
        return hydrosphere


@app.get("/rainfall")
def get_rainfall(
    country: int | None = None,
    year: int | None = None,
):
    with session_factory.begin() as session:
        statement = sql.select(
            db.Hydrosphere.country_id,
            db.Hydrosphere.year,
            db.Hydrosphere.average_rainfall,
        )
        if country is not None:
            statement = statement.where(db.Hydrosphere.country_id == country)
        if year is not None:
            statement = statement.where(db.Hydrosphere.year == year)
        rainfall = session.execute(statement)
        rainfall = [
            {"country": country_id, "year": year_, "average_rainfall": average_rainfall}
            for country_id, year_, average_rainfall in rainfall
        ]
        return rainfall


@app.get("/disasters")
def get_disasters(
    country: int | None = None,
    year: int | None = None,
):
    with session_factory.begin() as session:
        statement = sql.select(
            db.Disaster.country_id,
            db.Disaster.year,
            db.Disaster.extreme_weather_events,
        )
        if country is not None:
            statement = statement.where(db.Disaster.country_id == country)
        if year is not None:
            statement = statement.where(db.Disaster.year == year)
        disasters = session.execute(statement)
        disasters = [
            {
                "country": country_id,
                "year": year_,
                "extreme_weather_events": extreme_weather_events,
            }
            for country_id, year_, extreme_weather_events in disasters
        ]
        return disasters


@app.get("/forests")
def get_forests(
    country: int | None = None,
    year: int | None = None,
):
    with session_factory.begin() as session:
        statement = sql.select(
            db.Forest.country_id,
            db.Forest.year,
            db.Forest.forest_area,
            db.Forest.deforestation_rate,
        )
        if country is not None:
            statement = statement.where(db.Forest.country_id == country)
        if year is not None:
            statement = statement.where(db.Forest.year == year)
        forests = session.execute(statement)
        forests = [
            {
                "country": country_id,
                "year": year_,
                "forest_area": forest_area,
                "deforestation_rate": deforestation_rate,
            }
            for country_id, year_, forest_area, deforestation_rate in forests
        ]
        return forests


if __name__ == "__main__":
    uvicorn.run(app=app, host="0.0.0.0", port=8000)
