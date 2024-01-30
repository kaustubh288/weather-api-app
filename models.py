from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date, Float, PrimaryKeyConstraint

from database import Base


class Weather(Base):
    __tablename__ = 'weather'
    date = Column(Date)
    maximum_temp = Column(Integer)
    minimum_temp = Column(Integer)
    precipitation = Column(Integer)
    station = Column(String)
    __table_args__ = (
        PrimaryKeyConstraint(
            date,
            station
        ),
    )


class Analysis(Base):
    __tablename__ = 'analysis'
    avg_max_temperature = Column(Float)
    avg_min_temperature = Column(Float)
    total_precipitation = Column(Float)
    year = Column(Integer)
    station = Column(String)
    __table_args__ = (
        PrimaryKeyConstraint(
            year,
            station
        ),
    )

