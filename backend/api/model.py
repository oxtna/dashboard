from typing import Annotated
import pydantic as pdt

try:  # Production
    from .tags import Tags
except ImportError:  # Development
    from tags import Tags


class Country(pdt.BaseModel):
    id: Annotated[int, pdt.Field(ge=0, frozen=True)]
    name: Annotated[str, pdt.Field(frozen=True)]
    url: Annotated[pdt.HttpUrl, pdt.Field(frozen=True)]
    temperatures: Annotated[pdt.HttpUrl, pdt.Field(frozen=True)]
    population: Annotated[pdt.HttpUrl, pdt.Field(frozen=True)]
    gdp: Annotated[pdt.HttpUrl, pdt.Field(frozen=True)]
    pollution: Annotated[pdt.HttpUrl, pdt.Field(frozen=True)]
    energy: Annotated[pdt.HttpUrl, pdt.Field(frozen=True)]
    hydrosphere: Annotated[pdt.HttpUrl, pdt.Field(frozen=True)]
    rainfall: Annotated[pdt.HttpUrl, pdt.Field(frozen=True)]
    disasters: Annotated[pdt.HttpUrl, pdt.Field(frozen=True)]
    forests: Annotated[pdt.HttpUrl, pdt.Field(frozen=True)]
    tags: Annotated[
        list[Tags | str],
        pdt.Field(frozen=True, exclude=True),
    ] = [Tags.country]


class Temperature(pdt.BaseModel):
    year: Annotated[int, pdt.Field(ge=1900, frozen=True)]
    average_temperature: Annotated[float, pdt.Field(frozen=True)]
    temperature_anomaly: Annotated[float, pdt.Field(frozen=True)]
    country: Annotated[pdt.HttpUrl, pdt.Field(frozen=True)]
    tags: Annotated[
        list[Tags | str],
        pdt.Field(frozen=True, exclude=True),
    ] = [Tags.temperature]


class AverageTemperature(pdt.BaseModel):
    year: Annotated[int, pdt.Field(ge=1900, frozen=True)]
    average_temperature: Annotated[float, pdt.Field(frozen=True)]
    country: Annotated[pdt.HttpUrl, pdt.Field(frozen=True)]
    tags: Annotated[
        list[Tags | str],
        pdt.Field(frozen=True, exclude=True),
    ] = [Tags.temperature]


class TemperatureAnomaly(pdt.BaseModel):
    year: Annotated[int, pdt.Field(ge=1900, frozen=True)]
    temperature_anomaly: Annotated[float, pdt.Field(frozen=True)]
    country: Annotated[pdt.HttpUrl, pdt.Field(frozen=True)]
    tags: Annotated[
        list[Tags | str],
        pdt.Field(frozen=True, exclude=True),
    ] = [Tags.temperature]


class Population(pdt.BaseModel):
    year: Annotated[int, pdt.Field(ge=1900, frozen=True)]
    population: Annotated[float, pdt.Field(frozen=True)]
    country: Annotated[pdt.HttpUrl, pdt.Field(frozen=True)]
    tags: Annotated[
        list[Tags | str],
        pdt.Field(frozen=True, exclude=True),
    ] = [Tags.population]


class GDP(pdt.BaseModel):
    year: Annotated[int, pdt.Field(ge=1900, frozen=True)]
    gdp: Annotated[float, pdt.Field(frozen=True)]
    country: Annotated[pdt.HttpUrl, pdt.Field(frozen=True)]
    tags: Annotated[
        list[Tags | str],
        pdt.Field(frozen=True, exclude=True),
    ] = [Tags.gdp]


class Pollution(pdt.BaseModel):
    year: Annotated[int, pdt.Field(ge=1900, frozen=True)]
    co2_emissions: Annotated[float, pdt.Field(frozen=True)]
    methane_emissions: Annotated[float, pdt.Field(frozen=True)]
    air_pollution_index: Annotated[float, pdt.Field(frozen=True)]
    ocean_acidification: Annotated[float, pdt.Field(frozen=True)]
    per_capita_emissions: Annotated[float, pdt.Field(frozen=True)]
    country: Annotated[pdt.HttpUrl, pdt.Field(frozen=True)]
    tags: Annotated[
        list[Tags | str],
        pdt.Field(frozen=True, exclude=True),
    ] = [Tags.pollution]


class CO2Emissions(pdt.BaseModel):
    year: Annotated[int, pdt.Field(ge=1900, frozen=True)]
    co2_emissions: Annotated[float, pdt.Field(frozen=True)]
    country: Annotated[pdt.HttpUrl, pdt.Field(frozen=True)]
    tags: Annotated[
        list[Tags | str],
        pdt.Field(frozen=True, exclude=True),
    ] = [Tags.pollution]


class MethaneEmissions(pdt.BaseModel):
    year: Annotated[int, pdt.Field(ge=1900, frozen=True)]
    methane_emissions: Annotated[float, pdt.Field(frozen=True)]
    country: Annotated[pdt.HttpUrl, pdt.Field(frozen=True)]
    tags: Annotated[
        list[Tags | str],
        pdt.Field(frozen=True, exclude=True),
    ] = [Tags.pollution]


class AirPollutionIndex(pdt.BaseModel):
    year: Annotated[int, pdt.Field(ge=1900, frozen=True)]
    air_pollution_index: Annotated[float, pdt.Field(frozen=True)]
    country: Annotated[pdt.HttpUrl, pdt.Field(frozen=True)]
    tags: Annotated[
        list[Tags | str],
        pdt.Field(frozen=True, exclude=True),
    ] = [Tags.pollution]


class OceanAcidification(pdt.BaseModel):
    year: Annotated[int, pdt.Field(ge=1900, frozen=True)]
    ocean_acidification: Annotated[float, pdt.Field(frozen=True)]
    country: Annotated[pdt.HttpUrl, pdt.Field(frozen=True)]
    tags: Annotated[
        list[Tags | str],
        pdt.Field(frozen=True, exclude=True),
    ] = [Tags.pollution]


class PerCapitaEmissions(pdt.BaseModel):
    year: Annotated[int, pdt.Field(ge=1900, frozen=True)]
    per_capita_emissions: Annotated[float, pdt.Field(frozen=True)]
    country: Annotated[pdt.HttpUrl, pdt.Field(frozen=True)]
    tags: Annotated[
        list[Tags | str],
        pdt.Field(frozen=True, exclude=True),
    ] = [Tags.pollution]


class Energy(pdt.BaseModel):
    year: Annotated[int, pdt.Field(ge=1900, frozen=True)]
    renewable_energy_usage: Annotated[float, pdt.Field(frozen=True)]
    solar_energy_potential: Annotated[float, pdt.Field(frozen=True)]
    fossil_fuel_usage: Annotated[float, pdt.Field(frozen=True)]
    energy_consumption_per_capita: Annotated[float, pdt.Field(frozen=True)]
    country: Annotated[pdt.HttpUrl, pdt.Field(frozen=True)]
    tags: Annotated[
        list[Tags | str],
        pdt.Field(frozen=True, exclude=True),
    ] = [Tags.energy]


class Hydrosphere(pdt.BaseModel):
    year: Annotated[int, pdt.Field(ge=1900, frozen=True)]
    sea_level_rise: Annotated[float, pdt.Field(frozen=True)]
    arctic_ice_extent: Annotated[float, pdt.Field(frozen=True)]
    average_rainfall: Annotated[float, pdt.Field(frozen=True)]
    country: Annotated[pdt.HttpUrl, pdt.Field(frozen=True)]
    tags: Annotated[
        list[Tags | str],
        pdt.Field(frozen=True, exclude=True),
    ] = [Tags.hydrosphere]


class Rainfall(pdt.BaseModel):
    year: Annotated[int, pdt.Field(ge=1900, frozen=True)]
    average_rainfall: Annotated[float, pdt.Field(frozen=True)]
    country: Annotated[pdt.HttpUrl, pdt.Field(frozen=True)]
    tags: Annotated[
        list[Tags | str],
        pdt.Field(frozen=True, exclude=True),
    ] = [Tags.hydrosphere]


class Disaster(pdt.BaseModel):
    year: Annotated[int, pdt.Field(ge=1900, frozen=True)]
    extreme_weather_events: Annotated[int, pdt.Field(ge=0, frozen=True)]
    country: Annotated[pdt.HttpUrl, pdt.Field(frozen=True)]
    tags: Annotated[
        list[Tags | str],
        pdt.Field(frozen=True, exclude=True),
    ] = [Tags.disaster]


class Forest(pdt.BaseModel):
    year: Annotated[int, pdt.Field(ge=1900, frozen=True)]
    forest_area: Annotated[float, pdt.Field(frozen=True)]
    deforestation_rate: Annotated[float, pdt.Field(frozen=True)]
    country: Annotated[pdt.HttpUrl, pdt.Field(frozen=True)]
    tags: Annotated[
        list[Tags | str],
        pdt.Field(frozen=True, exclude=True),
    ] = [Tags.forest]
