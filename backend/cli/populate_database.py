import sqlalchemy.orm as orm
import pandas as pd
import db


def populate_database(
    session_factory: orm.sessionmaker[orm.Session], data_files: list[str]
) -> None:
    if len(data_files) == 0:
        return
    for file in data_files:
        file_df = pd.read_csv(
            file,
            delimiter=",",
            header=None,
            names=[
                "country",
                "year",
                "temperature_anomaly",
                "co2_emissions",
                "population",
                "forest_area",
                "gdp",
                "renewable_energy_usage",
                "methane_emissions",
                "sea_level_rise",
                "arctic_ice_extent",
                "urbanization",
                "deforestation_rate",
                "extreme_weather_events",
                "average_rainfall",
                "solar_energy_potential",
                "waste_management",
                "per_capita_emissions",
                "industrial_activity",
                "air_pollution_index",
                "biodiversity_index",
                "ocean_acidification",
                "fossil_fuel_usage",
                "energy_consumption_per_capita",
                "policy_score",
                "average_temperature",
            ],
            encoding="utf-8",
        )

        country_df = file_df[["country"]].drop_duplicates(keep="first")
        country_df.rename(columns={"country": "name"}, inplace=True)
        country_df.reset_index(drop=True, inplace=True)
        country_df["id"] = country_df.index
        with session_factory.begin() as session:
            countries = [
                db.Country(id=row["id"], name=row["name"])
                for _, row in country_df.iterrows()
            ]
            session.add_all(countries)
        country_df.set_index("name", inplace=True)

        temperature_df = file_df[
            [
                "country",
                "year",
                "temperature_anomaly",
                "average_temperature",
            ]
        ].copy()
        temperature_df.loc[:, "country"] = temperature_df["country"].map(
            country_df["id"]
        )
        temperature_df.rename(columns={"country": "country_id"}, inplace=True)
        with session_factory.begin() as session:
            temperatures = [
                db.Temperature(
                    country_id=row["country_id"],
                    year=row["year"],
                    temperature_anomaly=row["temperature_anomaly"],
                    average_temperature=row["average_temperature"],
                )
                for _, row in temperature_df.iterrows()
            ]
            session.add_all(temperatures)
        del temperature_df

        population_df = file_df[
            [
                "country",
                "year",
                "population",
                "gdp",
            ]
        ].copy()
        population_df.loc[:, "country"] = population_df["country"].map(country_df["id"])
        population_df.rename(columns={"country": "country_id"}, inplace=True)
        with session_factory.begin() as session:
            populations = [
                db.Population(
                    country_id=row["country_id"],
                    year=row["year"],
                    population=row["population"],
                    gdp=row["gdp"],
                )
                for _, row in population_df.iterrows()
            ]
            session.add_all(populations)
        del population_df

        pollution_df = file_df[
            [
                "country",
                "year",
                "co2_emissions",
                "methane_emissions",
                "air_pollution_index",
                "ocean_acidification",
                "per_capita_emissions",
            ]
        ].copy()
        pollution_df.loc[:, "country"] = pollution_df["country"].map(country_df["id"])
        pollution_df.rename(columns={"country": "country_id"}, inplace=True)
        with session_factory.begin() as session:
            pollutions = [
                db.Pollution(
                    country_id=row["country_id"],
                    year=row["year"],
                    co2_emissions=row["co2_emissions"],
                    methane_emissions=row["methane_emissions"],
                    air_pollution_index=row["air_pollution_index"],
                    ocean_acidification=row["ocean_acidification"],
                    per_capita_emissions=row["per_capita_emissions"],
                )
                for _, row in pollution_df.iterrows()
            ]
            session.add_all(pollutions)
        del pollution_df

        energy_df = file_df[
            [
                "country",
                "year",
                "renewable_energy_usage",
                "solar_energy_potential",
                "fossil_fuel_usage",
                "energy_consumption_per_capita",
            ]
        ].copy()
        energy_df.loc[:, "country"] = energy_df["country"].map(country_df["id"])
        energy_df.rename(columns={"country": "country_id"}, inplace=True)
        with session_factory.begin() as session:
            energies = [
                db.Energy(
                    country_id=row["country_id"],
                    year=row["year"],
                    renewable_energy_usage=row["renewable_energy_usage"],
                    solar_energy_potential=row["solar_energy_potential"],
                    fossil_fuel_usage=row["fossil_fuel_usage"],
                    energy_consumption_per_capita=row["energy_consumption_per_capita"],
                )
                for _, row in energy_df.iterrows()
            ]
            session.add_all(energies)
        del energy_df

        hydrosphere_df = file_df[
            [
                "country",
                "year",
                "sea_level_rise",
                "arctic_ice_extent",
                "average_rainfall",
            ]
        ].copy()
        hydrosphere_df.loc[:, "country"] = hydrosphere_df["country"].map(
            country_df["id"]
        )
        hydrosphere_df.rename(columns={"country": "country_id"}, inplace=True)
        with session_factory.begin() as session:
            hydrospheres = [
                db.Hydrosphere(
                    country_id=row["country_id"],
                    year=row["year"],
                    sea_level_rise=row["sea_level_rise"],
                    arctic_ice_extent=row["arctic_ice_extent"],
                    average_rainfall=row["average_rainfall"],
                )
                for _, row in hydrosphere_df.iterrows()
            ]
            session.add_all(hydrospheres)
        del hydrosphere_df

        disaster_df = file_df[
            [
                "country",
                "year",
                "extreme_weather_events",
            ]
        ].copy()
        disaster_df.loc[:, "country"] = disaster_df["country"].map(country_df["id"])
        disaster_df.rename(columns={"country": "country_id"}, inplace=True)
        with session_factory.begin() as session:
            disasters = [
                db.Disaster(
                    country_id=row["country_id"],
                    year=row["year"],
                    extreme_weather_events=row["extreme_weather_events"],
                )
                for _, row in disaster_df.iterrows()
            ]
            session.add_all(disasters)
        del disaster_df

        forest_df = file_df[
            [
                "country",
                "year",
                "forest_area",
                "deforestation_rate",
            ]
        ].copy()
        forest_df.loc[:, "country"] = forest_df["country"].map(country_df["id"])
        forest_df.rename(columns={"country": "country_id"}, inplace=True)
        with session_factory.begin() as session:
            forests = [
                db.Forest(
                    country_id=row["country_id"],
                    year=row["year"],
                    forest_area=row["forest_area"],
                    deforestation_rate=row["deforestation_rate"],
                )
                for _, row in forest_df.iterrows()
            ]
            session.add_all(forests)
        del forest_df
