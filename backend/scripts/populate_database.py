import argparse
import sqlalchemy as sql
import pandas as pd

POSTGRES_USERNAME = "dashboard"
POSTGRES_PASSWORD = "db123"
POSTGRES_DATABASE = "dashboard"
POSTGRES_HOST = "localhost"
POSTGRES_PORT = 8002

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Python script for populating a database."
    )
    parser.add_argument(
        "files",
        action="store",
        type=str,
        nargs="+",
        metavar="file",
        help="Filenames of csv files containing data following the database's schema.",
    )
    args = parser.parse_args()
    files: list[str] = args.files
    engine = sql.create_engine(
        f"postgresql+psycopg2://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DATABASE}"
    )
    for file in files:
        data_file = pd.read_csv(
            file,
            delimiter=",",
            header=None,
            names=[
                "Country",
                "Year",
                "Temperature_Anomaly",
                "CO2_Emissions",
                "Population",
                "Forest_Area",
                "GDP",
                "Renewable_Energy_Usage",
                "Methane_Emissions",
                "Sea_Level_Rise",
                "Arctic_Ice_Extent",
                "Urbanization",
                "Deforestation_Rate",
                "Extreme_Weather_Events",
                "Average_Rainfall",
                "Solar_Energy_Potential",
                "Waste_Management",
                "Per_Capita_Emissions",
                "Industrial_Activity",
                "Air_Pollution_Index",
                "Biodiversity_Index",
                "Ocean_Acidification",
                "Fossil_Fuel_Usage",
                "Energy_Consumption_Per_Capita",
                "Policy_Score",
                "Average_Temperature",
            ],
            encoding="utf-8",
        )
        countries = data_file[["Country"]].drop_duplicates(keep="first")
        countries.rename(columns={"Country": "Name"}, inplace=True)
        countries.reset_index(drop=True, inplace=True)
        countries["Index"] = countries.index
        countries.to_sql("Countries", con=engine, index=False, if_exists="replace")
        countries.set_index("Name", inplace=True)
        temperatures = data_file[
            [
                "Country",
                "Year",
                "Temperature_Anomaly",
                "Average_Temperature",
            ]
        ].copy()
        temperatures.loc[:, "Country"] = temperatures["Country"].map(countries["Index"])
        temperatures.rename(columns={"Country": "CountryIndex"}, inplace=True)
        temperatures.to_sql("Temperatures", con=engine, index=True, if_exists="replace")
        del temperatures
        population = data_file[
            [
                "Country",
                "Year",
                "Population",
                "GDP",
            ]
        ].copy()
        population.loc[:, "Country"] = population["Country"].map(countries["Index"])
        population.rename(columns={"Country": "CountryIndex"}, inplace=True)
        population.to_sql("Population", con=engine, index=True, if_exists="replace")
        del population
        pollution = data_file[
            [
                "Country",
                "Year",
                "CO2_Emissions",
                "Methane_Emissions",
                "Air_Pollution_Index",
                "Ocean_Acidification",
                "Per_Capita_Emissions",
            ]
        ].copy()
        pollution.loc[:, "Country"] = pollution["Country"].map(countries["Index"])
        pollution.rename(columns={"Country": "CountryIndex"}, inplace=True)
        pollution.to_sql("Pollution", con=engine, index=True, if_exists="replace")
        del pollution
        energy = data_file[
            [
                "Country",
                "Year",
                "Renewable_Energy_Usage",
                "Solar_Energy_Potential",
                "Fossil_Fuel_Usage",
                "Energy_Consumption_Per_Capita",
            ]
        ].copy()
        energy.loc[:, "Country"] = energy["Country"].map(countries["Index"])
        energy.rename(columns={"Country": "CountryIndex"}, inplace=True)
        energy.to_sql("Energy", con=engine, index=True, if_exists="replace")
        del energy
        hydrosphere = data_file[
            [
                "Country",
                "Year",
                "Sea_Level_Rise",
                "Arctic_Ice_Extent",
                "Average_Rainfall",
            ]
        ].copy()
        hydrosphere.loc[:, "Country"] = hydrosphere["Country"].map(countries["Index"])
        hydrosphere.rename(columns={"Country": "CountryIndex"}, inplace=True)
        hydrosphere.to_sql("Hydrosphere", con=engine, index=True, if_exists="replace")
        del hydrosphere
        disasters = data_file[
            [
                "Country",
                "Year",
                "Extreme_Weather_Events",
            ]
        ].copy()
        disasters.loc[:, "Country"] = disasters["Country"].map(countries["Index"])
        disasters.rename(columns={"Country": "CountryIndex"}, inplace=True)
        disasters.to_sql("Disasters", con=engine, index=True, if_exists="replace")
        del disasters
        forests = data_file[
            [
                "Country",
                "Year",
                "Forest_Area",
                "Deforestation_Rate",
            ]
        ].copy()
        forests.loc[:, "Country"] = forests["Country"].map(countries["Index"])
        forests.rename(columns={"Country": "CountryIndex"}, inplace=True)
        forests.to_sql("Forests", con=engine, index=True, if_exists="replace")
        del forests
        del countries
