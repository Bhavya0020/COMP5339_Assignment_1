import duckdb
import pandas as pd
import os

def store_to_duckdb(fuel_df):
    os.makedirs("db", exist_ok=True)
    con = duckdb.connect("db/fuelcheck.duckdb")

    # Drop existing tables and sequence
    con.execute("DROP TABLE IF EXISTS fuel_data")
    con.execute("DROP TABLE IF EXISTS FUEL_DETAILS")
    con.execute("DROP TABLE IF EXISTS GEO_MAPPING")
    con.execute("DROP SEQUENCE IF EXISTS station_id_seq")

    # Create sequence
    con.execute("CREATE SEQUENCE station_id_seq START 1")

    # Create FUEL_DETAILS table
    con.execute("""
        CREATE TABLE FUEL_DETAILS (
            FuelCode VARCHAR(3) PRIMARY KEY,
            FuelType VARCHAR(20) NOT NULL,
            Sales DECIMAL(10, 2),
            Month VARCHAR(10)
        );
    """)

    # Create GEO_MAPPING table
    con.execute("""
        CREATE TABLE GEO_MAPPING (
            Address VARCHAR(100) PRIMARY KEY,
            Latitude DECIMAL(9,6) NOT NULL,
            Longitude DECIMAL(9,6) NOT NULL,
            OpeningTime TIME NULL,
            ClosingTime TIME NULL
        );
    """)

    # Create main fuel_data table with foreign keys
    con.execute("""
        CREATE TABLE fuel_data (
            station_tracking_id INTEGER DEFAULT nextval('station_id_seq') PRIMARY KEY,
            servicestationname TEXT,
            Address VARCHAR(100),
            suburb TEXT,
            postcode INTEGER,
            brand TEXT,
            fuelcode VARCHAR(3),
            priceupdateddate TIMESTAMP,
            price FLOAT,
        );
    """)

    # FOREIGN KEY (fuelcode) REFERENCES FUEL_DETAILS(FuelCode),
    # FOREIGN KEY (address) REFERENCES GEO_MAPPING(Address)

    # Register and insert data (you can adjust/remove the LIMIT as needed)
    con.register("fuel_df", fuel_df)
    con.execute("""
            INSERT INTO fuel_data (
                servicestationname,
                address,
                suburb,
                postcode,
                brand,
                fuelcode,
                priceupdateddate,
                price
            )
            SELECT * FROM fuel_df LIMIT 100
            """
        )

    con.close()
    print("💾 Schema and data stored in db/fuelcheck.duckdb")

if __name__ == "__main__":
    df = pd.read_csv(
        "/Users/bhavyadhingra/Desktop/USYD_Study/SEM_3/Data Engineering/COMP5339_Assignment_1/cleaned_fuelcheck_data.csv",
        low_memory=False
    )
    print(df.head())
    print(df.columns)
    store_to_duckdb(df)
