from sqlalchemy import Table, Column, Integer, String, TIMESTAMP, MetaData


metadata = MetaData()

# create Table Model for Database
operation = Table(
    "operation",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("quantity", String),
    Column("figi", String),
    Column("instrument_type", String, nullable=True),
    Column("date", TIMESTAMP),
    Column("type", String),
)
