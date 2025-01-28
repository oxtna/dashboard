import argparse
import sqlalchemy as sql
import pandas as pd

TABLE_NAME = "Global_Warming"

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
    parser.add_argument(
        "-r",
        "--reset",
        action="store_true",
        help="Flag to remove all entries from the table",
    )
    args = parser.parse_args()
    files: list[str] = args.files
    should_reset: bool = args.reset
    engine = sql.create_engine(
        "postgresql+psycopg2://dashboard:db123@localhost:8002/dashboard"
    )
    if should_reset:
        if TABLE_NAME in sql.inspect(engine).get_table_names():
            with engine.connect() as connection:
                delete_query = sql.Table(
                    TABLE_NAME, sql.MetaData(), autoload_with=engine
                ).delete()
                connection.execute(delete_query)
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
        data_file.to_sql(TABLE_NAME, con=engine, if_exists="append")
