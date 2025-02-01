from typing import Annotated
from fastapi import FastAPI, Request, Query, Path
import uvicorn
import pydantic as pdt
import sqlalchemy as sql
import sqlalchemy.orm as orm
import db
from .tags import Tags
from .model import *
from .filter import FilterParams, CountriesFilterParams

app = FastAPI(title="Dashboard API", root_path="/api/v1")
engine = sql.create_engine(
    f"postgresql+psycopg2://\
{db.USERNAME}:{db.PASSWORD}@\
{db.CONTAINER_HOST}:{db.CONTAINER_PORT}/\
{db.DATABASE_NAME}",
    pool_pre_ping=True,
)
session_factory = orm.sessionmaker(bind=engine)


@app.get("/countries", tags=[Tags.country])
def get_countries(
    filter_query: Annotated[CountriesFilterParams, Query()],
    request: Request,
) -> list[Country]:
    with session_factory.begin() as session:
        statement = sql.select(db.Country.id, db.Country.name)
        statement = statement.order_by(None)
        # Default ordering first
        if filter_query.order_by == "id":
            statement = statement.order_by(db.Country.id)
        else:
            statement = statement.order_by(db.Country.name)
        countries = session.execute(statement)
        countries = countries.scalars().all()
        countries = [
            Country(
                id=country_id,
                name=name,
                url=pdt.HttpUrl(f"{request.base_url}countries/{country_id}"),
                temperatures=pdt.HttpUrl(
                    f"{request.base_url}temperatures?country={country_id}"
                ),
                population=pdt.HttpUrl(
                    f"{request.base_url}population?country={country_id}"
                ),
                gdp=pdt.HttpUrl(f"{request.base_url}gdp?country={country_id}"),
                pollution=pdt.HttpUrl(
                    f"{request.base_url}pollution?country={country_id}"
                ),
                energy=pdt.HttpUrl(f"{request.base_url}energy?country={country_id}"),
                hydrosphere=pdt.HttpUrl(
                    f"{request.base_url}hydrosphere?country={country_id}"
                ),
                rainfall=pdt.HttpUrl(
                    f"{request.base_url}rainfall?country={country_id}"
                ),
                disasters=pdt.HttpUrl(
                    f"{request.base_url}disasters?country={country_id}"
                ),
                forests=pdt.HttpUrl(f"{request.base_url}forests?country={country_id}"),
            )
            for country_id, name in countries
        ]
        return countries


@app.get("/countries/{country_id}", tags=[Tags.country])
def get_country(
    country_id: Annotated[int, Path(ge=0, title="ID of the country to get")],
    request: Request,
) -> Country | None:
    with session_factory.begin() as session:
        statement = sql.select(db.Country).where(db.Country.id == country_id)
        country = session.execute(statement)
        country = country.scalar_one_or_none()
        if country is None:
            return None
        return Country(
            id=country.id,
            name=country.name,
            url=pdt.HttpUrl(f"{request.base_url}countries/{country_id}"),
            temperatures=pdt.HttpUrl(
                f"{request.base_url}temperatures?country={country_id}"
            ),
            population=pdt.HttpUrl(
                f"{request.base_url}population?country={country_id}"
            ),
            gdp=pdt.HttpUrl(f"{request.base_url}gdp?country={country_id}"),
            pollution=pdt.HttpUrl(f"{request.base_url}pollution?country={country_id}"),
            energy=pdt.HttpUrl(f"{request.base_url}energy?country={country_id}"),
            hydrosphere=pdt.HttpUrl(
                f"{request.base_url}hydrosphere?country={country_id}"
            ),
            rainfall=pdt.HttpUrl(f"{request.base_url}rainfall?country={country_id}"),
            disasters=pdt.HttpUrl(f"{request.base_url}disasters?country={country_id}"),
            forests=pdt.HttpUrl(f"{request.base_url}forests?country={country_id}"),
        )


@app.get("/temperatures", tags=[Tags.temperature])
def get_temperatures(
    filter_query: Annotated[FilterParams, Query()],
    request: Request,
) -> list[Temperature]:
    with session_factory.begin() as session:
        statement = sql.select(
            db.Temperature.country_id,
            db.Temperature.year,
            db.Temperature.average_temperature,
            db.Temperature.temperature_anomaly,
        )
        if filter_query.country is not None:
            statement = statement.where(
                db.Temperature.country_id == filter_query.country
            )
        if filter_query.year is not None:
            statement = statement.where(db.Temperature.year == filter_query.year)
        statement = statement.order_by(None)
        # Default ordering first
        if filter_query.order_by == "year":
            statement = statement.order_by(db.Temperature.year)
        else:
            statement = statement.order_by(db.Temperature.country_id)
        temperatures = session.execute(statement)
        temperatures = [
            Temperature(
                country=pdt.HttpUrl(f"{request.base_url}countries/{country_id}"),
                year=year_,
                average_temperature=average_temperature,
                temperature_anomaly=temperature_anomaly,
            )
            for country_id, year_, average_temperature, temperature_anomaly in temperatures
        ]
        return temperatures


@app.get("/temperatures/average", tags=[Tags.temperature])
def get_average_temperatures(
    filter_query: Annotated[FilterParams, Query()],
    request: Request,
) -> list[AverageTemperature]:
    with session_factory.begin() as session:
        statement = sql.select(
            db.Temperature.country_id,
            db.Temperature.year,
            db.Temperature.average_temperature,
        )
        if filter_query.country is not None:
            statement = statement.where(
                db.Temperature.country_id == filter_query.country
            )
        if filter_query.year is not None:
            statement = statement.where(db.Temperature.year == filter_query.year)
        statement = statement.order_by(None)
        # Default ordering first
        if filter_query.order_by == "year":
            statement = statement.order_by(db.Temperature.year)
        else:
            statement = statement.order_by(db.Temperature.country_id)
        average_temperatures = session.execute(statement)
        average_temperatures = [
            AverageTemperature(
                country=pdt.HttpUrl(f"{request.base_url}countries/{country_id}"),
                year=year_,
                average_temperature=average_temperature,
            )
            for country_id, year_, average_temperature in average_temperatures
        ]
        return average_temperatures


@app.get("/temperatures/anomaly", tags=[Tags.temperature])
def get_temperature_anomalies(
    filter_query: Annotated[FilterParams, Query()],
    request: Request,
) -> list[TemperatureAnomaly]:
    with session_factory.begin() as session:
        statement = sql.select(
            db.Temperature.country_id,
            db.Temperature.year,
            db.Temperature.temperature_anomaly,
        )
        if filter_query.country is not None:
            statement = statement.where(
                db.Temperature.country_id == filter_query.country
            )
        if filter_query.year is not None:
            statement = statement.where(db.Temperature.year == filter_query.year)
        statement = statement.order_by(None)
        # Default ordering first
        if filter_query.order_by == "year":
            statement = statement.order_by(db.Temperature.year)
        else:
            statement = statement.order_by(db.Temperature.country_id)
        temperature_anomalies = session.execute(statement)
        temperature_anomalies = [
            TemperatureAnomaly(
                country=pdt.HttpUrl(f"{request.base_url}countries/{country_id}"),
                year=year_,
                temperature_anomaly=temperature_anomaly,
            )
            for country_id, year_, temperature_anomaly in temperature_anomalies
        ]
        return temperature_anomalies


@app.get("/population", tags=[Tags.population])
def get_population(
    filter_query: Annotated[FilterParams, Query()],
    request: Request,
) -> list[Population]:
    with session_factory.begin() as session:
        statement = sql.select(
            db.Population.country_id,
            db.Population.year,
            db.Population.population,
        )
        if filter_query.country is not None:
            statement = statement.where(
                db.Population.country_id == filter_query.country
            )
        if filter_query.year is not None:
            statement = statement.where(db.Population.year == filter_query.year)
        statement = statement.order_by(None)
        # Default ordering first
        if filter_query.order_by == "year":
            statement = statement.order_by(db.Population.year)
        else:
            statement = statement.order_by(db.Population.country_id)
        population = session.execute(statement)
        population = [
            Population(
                country=pdt.HttpUrl(f"{request.base_url}countries/{country_id}"),
                year=year_,
                population=population_,
            )
            for country_id, year_, population_ in population
        ]
        return population


@app.get("/gdp", tags=[Tags.gdp])
def get_gdp(
    filter_query: Annotated[FilterParams, Query()],
    request: Request,
) -> list[GDP]:
    with session_factory.begin() as session:
        statement = sql.select(
            db.Population.country_id,
            db.Population.year,
            db.Population.gdp,
        )
        if filter_query.country is not None:
            statement = statement.where(
                db.Population.country_id == filter_query.country
            )
        if filter_query.year is not None:
            statement = statement.where(db.Population.year == filter_query.year)
        statement = statement.order_by(None)
        # Default ordering first
        if filter_query.order_by == "year":
            statement = statement.order_by(db.Population.year)
        else:
            statement = statement.order_by(db.Population.country_id)
        gdp = session.execute(statement)
        gdp = [
            GDP(
                country=pdt.HttpUrl(f"{request.base_url}countries/{country_id}"),
                year=year_,
                gdp=gdp_,
            )
            for country_id, year_, gdp_ in gdp
        ]
        return gdp


@app.get("/pollution", tags=[Tags.pollution])
def get_pollution(
    filter_query: Annotated[FilterParams, Query()],
    request: Request,
) -> list[Pollution]:
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
        if filter_query.country is not None:
            statement = statement.where(db.Pollution.country_id == filter_query.country)
        if filter_query.year is not None:
            statement = statement.where(db.Pollution.year == filter_query.year)
        statement = statement.order_by(None)
        # Default ordering first
        if filter_query.order_by == "year":
            statement = statement.order_by(db.Pollution.year)
        else:
            statement = statement.order_by(db.Pollution.country_id)
        pollution = session.execute(statement)
        pollution = [
            Pollution(
                country=pdt.HttpUrl(f"{request.base_url}countries/{country_id}"),
                year=year_,
                co2_emissions=co2_emissions,
                methane_emissions=methane_emissions,
                air_pollution_index=air_pollution_index,
                ocean_acidification=ocean_acidification,
                per_capita_emissions=per_capita_emissions,
            )
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


@app.get("/pollution/co2", tags=[Tags.pollution])
def get_co2_emissions(
    filter_query: Annotated[FilterParams, Query()],
    request: Request,
) -> list[CO2Emissions]:
    with session_factory.begin() as session:
        statement = sql.select(
            db.Pollution.country_id,
            db.Pollution.year,
            db.Pollution.co2_emissions,
        )
        if filter_query.country is not None:
            statement = statement.where(db.Pollution.country_id == filter_query.country)
        if filter_query.year is not None:
            statement = statement.where(db.Pollution.year == filter_query.year)
        statement = statement.order_by(None)
        # Default ordering first
        if filter_query.order_by == "year":
            statement = statement.order_by(db.Pollution.year)
        else:
            statement = statement.order_by(db.Pollution.country_id)
        co2_emissions = session.execute(statement)
        co2_emissions = [
            CO2Emissions(
                country=pdt.HttpUrl(f"{request.base_url}countries/{country_id}"),
                year=year_,
                co2_emissions=co2_emissions_,
            )
            for country_id, year_, co2_emissions_ in co2_emissions
        ]
        return co2_emissions


@app.get("/pollution/methane", tags=[Tags.pollution])
def get_methane_emissions(
    filter_query: Annotated[FilterParams, Query()],
    request: Request,
) -> list[MethaneEmissions]:
    with session_factory.begin() as session:
        statement = sql.select(
            db.Pollution.country_id,
            db.Pollution.year,
            db.Pollution.methane_emissions,
        )
        if filter_query.country is not None:
            statement = statement.where(db.Pollution.country_id == filter_query.country)
        if filter_query.year is not None:
            statement = statement.where(db.Pollution.year == filter_query.year)
        statement = statement.order_by(None)
        # Default ordering first
        if filter_query.order_by == "year":
            statement = statement.order_by(db.Pollution.year)
        else:
            statement = statement.order_by(db.Pollution.country_id)
        methane_emissions = session.execute(statement)
        methane_emissions = [
            MethaneEmissions(
                country=pdt.HttpUrl(f"{request.base_url}countries/{country_id}"),
                year=year_,
                methane_emissions=methane_emissions_,
            )
            for country_id, year_, methane_emissions_ in methane_emissions
        ]
        return methane_emissions


@app.get("/pollution/air-pollution-index", tags=[Tags.pollution])
def get_air_pollution_index(
    filter_query: Annotated[FilterParams, Query()],
    request: Request,
) -> list[AirPollutionIndex]:
    with session_factory.begin() as session:
        statement = sql.select(
            db.Pollution.country_id,
            db.Pollution.year,
            db.Pollution.air_pollution_index,
        )
        if filter_query.country is not None:
            statement = statement.where(db.Pollution.country_id == filter_query.country)
        if filter_query.year is not None:
            statement = statement.where(db.Pollution.year == filter_query.year)
        statement = statement.order_by(None)
        # Default ordering first
        if filter_query.order_by == "year":
            statement = statement.order_by(db.Pollution.year)
        else:
            statement = statement.order_by(db.Pollution.country_id)
        air_pollution_index = session.execute(statement)
        air_pollution_index = [
            AirPollutionIndex(
                country=pdt.HttpUrl(f"{request.base_url}countries/{country_id}"),
                year=year_,
                air_pollution_index=air_pollution_index_,
            )
            for country_id, year_, air_pollution_index_ in air_pollution_index
        ]
        return air_pollution_index


@app.get("/pollution/ocean-acidification", tags=[Tags.pollution])
def get_ocean_acidification(
    filter_query: Annotated[FilterParams, Query()],
    request: Request,
) -> list[OceanAcidification]:
    with session_factory.begin() as session:
        statement = sql.select(
            db.Pollution.country_id,
            db.Pollution.year,
            db.Pollution.ocean_acidification,
        )
        if filter_query.country is not None:
            statement = statement.where(db.Pollution.country_id == filter_query.country)
        if filter_query.year is not None:
            statement = statement.where(db.Pollution.year == filter_query.year)
        statement = statement.order_by(None)
        # Default ordering first
        if filter_query.order_by == "year":
            statement = statement.order_by(db.Pollution.year)
        else:
            statement = statement.order_by(db.Pollution.country_id)
        ocean_acidification = session.execute(statement)
        ocean_acidification = [
            OceanAcidification(
                country=pdt.HttpUrl(f"{request.base_url}countries/{country_id}"),
                year=year_,
                ocean_acidification=ocean_acidification_,
            )
            for country_id, year_, ocean_acidification_ in ocean_acidification
        ]
        return ocean_acidification


@app.get("/pollution/per-capita", tags=[Tags.pollution])
def get_per_capita_emissions(
    filter_query: Annotated[FilterParams, Query()],
    request: Request,
) -> list[PerCapitaEmissions]:
    with session_factory.begin() as session:
        statement = sql.select(
            db.Pollution.country_id,
            db.Pollution.year,
            db.Pollution.per_capita_emissions,
        )
        if filter_query.country is not None:
            statement = statement.where(db.Pollution.country_id == filter_query.country)
        if filter_query.year is not None:
            statement = statement.where(db.Pollution.year == filter_query.year)
        statement = statement.order_by(None)
        # Default ordering first
        if filter_query.order_by == "year":
            statement = statement.order_by(db.Pollution.year)
        else:
            statement = statement.order_by(db.Pollution.country_id)
        per_capita_emissions = session.execute(statement)
        per_capita_emissions = [
            PerCapitaEmissions(
                country=pdt.HttpUrl(f"{request.base_url}countries/{country_id}"),
                year=year_,
                per_capita_emissions=per_capita_emissions_,
            )
            for country_id, year_, per_capita_emissions_ in per_capita_emissions
        ]
        return per_capita_emissions


@app.get("/energy", tags=[Tags.energy])
def get_energy(
    filter_query: Annotated[FilterParams, Query()],
    request: Request,
) -> list[Energy]:
    with session_factory.begin() as session:
        statement = sql.select(
            db.Energy.country_id,
            db.Energy.year,
            db.Energy.renewable_energy_usage,
            db.Energy.solar_energy_potential,
            db.Energy.fossil_fuel_usage,
            db.Energy.energy_consumption_per_capita,
        )
        if filter_query.country is not None:
            statement = statement.where(db.Energy.country_id == filter_query.country)
        if filter_query.year is not None:
            statement = statement.where(db.Energy.year == filter_query.year)
        statement = statement.order_by(None)
        # Default ordering first
        if filter_query.order_by == "year":
            statement = statement.order_by(db.Energy.year)
        else:
            statement = statement.order_by(db.Energy.country_id)
        energy = session.execute(statement)
        energy = [
            Energy(
                country=pdt.HttpUrl(f"{request.base_url}countries/{country_id}"),
                year=year_,
                renewable_energy_usage=renewable_energy_usage,
                solar_energy_potential=solar_energy_potential,
                fossil_fuel_usage=fossil_fuel_usage,
                energy_consumption_per_capita=energy_consumption_per_capita,
            )
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


@app.get("/hydrosphere", tags=[Tags.hydrosphere])
def get_hydrosphere(
    filter_query: Annotated[FilterParams, Query()],
    request: Request,
) -> list[Hydrosphere]:
    with session_factory.begin() as session:
        statement = sql.select(
            db.Hydrosphere.country_id,
            db.Hydrosphere.year,
            db.Hydrosphere.sea_level_rise,
            db.Hydrosphere.arctic_ice_extent,
            db.Hydrosphere.average_rainfall,
        )
        if filter_query.country is not None:
            statement = statement.where(
                db.Hydrosphere.country_id == filter_query.country
            )
        if filter_query.year is not None:
            statement = statement.where(db.Hydrosphere.year == filter_query.year)
        statement = statement.order_by(None)
        # Default ordering first
        if filter_query.order_by == "year":
            statement = statement.order_by(db.Hydrosphere.year)
        else:
            statement = statement.order_by(db.Hydrosphere.country_id)
        hydrosphere = session.execute(statement)
        hydrosphere = [
            Hydrosphere(
                country=pdt.HttpUrl(f"{request.base_url}countries/{country_id}"),
                year=year_,
                sea_level_rise=sea_level_rise,
                arctic_ice_extent=arctic_ice_extent,
                average_rainfall=average_rainfall,
            )
            for (
                country_id,
                year_,
                sea_level_rise,
                arctic_ice_extent,
                average_rainfall,
            ) in hydrosphere
        ]
        return hydrosphere


@app.get("/rainfall", tags=[Tags.hydrosphere])
def get_rainfall(
    filter_query: Annotated[FilterParams, Query()],
    request: Request,
) -> list[Rainfall]:
    with session_factory.begin() as session:
        statement = sql.select(
            db.Hydrosphere.country_id,
            db.Hydrosphere.year,
            db.Hydrosphere.average_rainfall,
        )
        if filter_query.country is not None:
            statement = statement.where(
                db.Hydrosphere.country_id == filter_query.country
            )
        if filter_query.year is not None:
            statement = statement.where(db.Hydrosphere.year == filter_query.year)
        statement = statement.order_by(None)
        # Default ordering first
        if filter_query.order_by == "year":
            statement = statement.order_by(db.Hydrosphere.year)
        else:
            statement = statement.order_by(db.Hydrosphere.country_id)
        rainfall = session.execute(statement)
        rainfall = [
            Rainfall(
                country=pdt.HttpUrl(f"{request.base_url}countries/{country_id}"),
                year=year_,
                average_rainfall=average_rainfall,
            )
            for country_id, year_, average_rainfall in rainfall
        ]
        return rainfall


@app.get("/disasters", tags=[Tags.disaster])
def get_disasters(
    filter_query: Annotated[FilterParams, Query()],
    request: Request,
) -> list[Disaster]:
    with session_factory.begin() as session:
        statement = sql.select(
            db.Disaster.country_id,
            db.Disaster.year,
            db.Disaster.extreme_weather_events,
        )
        if filter_query.country is not None:
            statement = statement.where(db.Disaster.country_id == filter_query.country)
        if filter_query.year is not None:
            statement = statement.where(db.Disaster.year == filter_query.year)
        statement = statement.order_by(None)
        # Default ordering first
        if filter_query.order_by == "year":
            statement = statement.order_by(db.Disaster.year)
        else:
            statement = statement.order_by(db.Disaster.country_id)
        disasters = session.execute(statement)
        disasters = [
            Disaster(
                country=pdt.HttpUrl(f"{request.base_url}countries/{country_id}"),
                year=year_,
                extreme_weather_events=extreme_weather_events,
            )
            for country_id, year_, extreme_weather_events in disasters
        ]
        return disasters


@app.get("/forests", tags=[Tags.forest])
def get_forests(
    filter_query: Annotated[FilterParams, Query()],
    request: Request,
) -> list[Forest]:
    with session_factory.begin() as session:
        statement = sql.select(
            db.Forest.country_id,
            db.Forest.year,
            db.Forest.forest_area,
            db.Forest.deforestation_rate,
        )
        if filter_query.country is not None:
            statement = statement.where(db.Forest.country_id == filter_query.country)
        if filter_query.year is not None:
            statement = statement.where(db.Forest.year == filter_query.year)
        statement = statement.order_by(None)
        # Default ordering first
        if filter_query.order_by == "year":
            statement = statement.order_by(db.Forest.year)
        else:
            statement = statement.order_by(db.Forest.country_id)
        forests = session.execute(statement)
        forests = [
            Forest(
                country=pdt.HttpUrl(f"{request.base_url}countries/{country_id}"),
                year=year_,
                forest_area=forest_area,
                deforestation_rate=deforestation_rate,
            )
            for country_id, year_, forest_area, deforestation_rate in forests
        ]
        return forests


if __name__ == "__main__":
    uvicorn.run(app=app, host="0.0.0.0", port=8000)
