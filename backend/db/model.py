import sqlalchemy as sql
import sqlalchemy.orm as orm


class Base(orm.DeclarativeBase):
    pass


class Country(Base):
    __tablename__ = "country"

    id: orm.Mapped[int] = orm.mapped_column(
        sql.Integer, primary_key=True, autoincrement=True
    )
    name: orm.Mapped[str] = orm.mapped_column(sql.String(32))

    temperatures: orm.Mapped[list["Temperature"]] = orm.relationship(
        back_populates="country"
    )
    population: orm.Mapped[list["Population"]] = orm.relationship(
        back_populates="country"
    )
    pollution: orm.Mapped[list["Pollution"]] = orm.relationship(
        back_populates="country"
    )
    energy: orm.Mapped[list["Energy"]] = orm.relationship(back_populates="country")
    hydrosphere: orm.Mapped[list["Hydrosphere"]] = orm.relationship(
        back_populates="country"
    )
    disasters: orm.Mapped[list["Disaster"]] = orm.relationship(back_populates="country")
    forests: orm.Mapped[list["Forest"]] = orm.relationship(back_populates="country")


class Temperature(Base):
    __tablename__ = "temperature"

    id: orm.Mapped[int] = orm.mapped_column(
        sql.Integer, primary_key=True, autoincrement=True
    )
    country_id: orm.Mapped[int] = orm.mapped_column(sql.ForeignKey("country.id"))
    year: orm.Mapped[int]
    temperature_anomaly: orm.Mapped[float]
    average_temperature: orm.Mapped[float]

    country: orm.Mapped[Country] = orm.relationship(back_populates="temperatures")


class Population(Base):
    __tablename__ = "population"

    id: orm.Mapped[int] = orm.mapped_column(
        sql.Integer, primary_key=True, autoincrement=True
    )
    country_id: orm.Mapped[int] = orm.mapped_column(sql.ForeignKey("country.id"))
    year: orm.Mapped[int]
    population: orm.Mapped[float]
    gdp: orm.Mapped[float]

    country: orm.Mapped[Country] = orm.relationship(back_populates="population")


class Pollution(Base):
    __tablename__ = "pollution"

    id: orm.Mapped[int] = orm.mapped_column(
        sql.Integer, primary_key=True, autoincrement=True
    )
    country_id: orm.Mapped[int] = orm.mapped_column(sql.ForeignKey("country.id"))
    year: orm.Mapped[int]
    co2_emissions: orm.Mapped[float]
    methane_emissions: orm.Mapped[float]
    air_pollution_index: orm.Mapped[float]
    ocean_acidification: orm.Mapped[float]
    per_capita_emissions: orm.Mapped[float]

    country: orm.Mapped[Country] = orm.relationship(back_populates="pollution")


class Energy(Base):
    __tablename__ = "energy"

    id: orm.Mapped[int] = orm.mapped_column(
        sql.Integer, primary_key=True, autoincrement=True
    )
    country_id: orm.Mapped[int] = orm.mapped_column(sql.ForeignKey("country.id"))
    year: orm.Mapped[int]
    renewable_energy_usage: orm.Mapped[float]
    solar_energy_potential: orm.Mapped[float]
    fossil_fuel_usage: orm.Mapped[float]
    energy_consumption_per_capita: orm.Mapped[float]

    country: orm.Mapped[Country] = orm.relationship(back_populates="energy")


class Hydrosphere(Base):
    __tablename__ = "hydrosphere"

    id: orm.Mapped[int] = orm.mapped_column(
        sql.Integer, primary_key=True, autoincrement=True
    )
    country_id: orm.Mapped[int] = orm.mapped_column(sql.ForeignKey("country.id"))
    year: orm.Mapped[int]
    sea_level_rise: orm.Mapped[float]
    arctic_ice_extent: orm.Mapped[float]
    average_rainfall: orm.Mapped[float]

    country: orm.Mapped[Country] = orm.relationship(back_populates="hydrosphere")


class Disaster(Base):
    __tablename__ = "disaster"

    id: orm.Mapped[int] = orm.mapped_column(
        sql.Integer, primary_key=True, autoincrement=True
    )
    country_id: orm.Mapped[int] = orm.mapped_column(sql.ForeignKey("country.id"))
    year: orm.Mapped[int]
    extreme_weather_events: orm.Mapped[int]

    country: orm.Mapped[Country] = orm.relationship(back_populates="disasters")


class Forest(Base):
    __tablename__ = "forest"

    id: orm.Mapped[int] = orm.mapped_column(
        sql.Integer, primary_key=True, autoincrement=True
    )
    country_id: orm.Mapped[int] = orm.mapped_column(sql.ForeignKey("country.id"))
    year: orm.Mapped[int]
    forest_area: orm.Mapped[float]
    deforestation_rate: orm.Mapped[float]

    country: orm.Mapped[Country] = orm.relationship(back_populates="forests")
