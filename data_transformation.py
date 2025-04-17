import duckdb
import pandas as pd
import os

def store_to_duckdb(fuel_df):
    os.makedirs("db", exist_ok=True)
    con = duckdb.connect("db/fuelcheck.duckdb")

    # Drop existing tables
    con.execute("DROP TABLE IF EXISTS fuel_data")
    # con.execute("DROP TABLE IF EXISTS station_locations")

    # Explicit schema creation
    con.execute("""
        CREATE TABLE fuel_data (
            station_id INTEGER,
            servicestationname TEXT,
            address TEXT,
            suburb TEXT,
            postcode INTEGER,
            brand TEXT,
            fuelcode TEXT,
            priceupdateddate TIMESTAMP,
            price FLOAT,
            source_file TEXT
        );

    """)

    # con.execute("""
    #     CREATE TABLE station_locations (
    #         station_id INTEGER,
    #         name TEXT,
    #         suburb TEXT,
    #         latitude DOUBLE,
    #         longitude DOUBLE
    #         -- Add more if needed
    #     )
    # """)

    # Register dataframes
    con.register("fuel_df", fuel_df)
    # con.register("location_df", location_df)

    # Insert data
    con.execute("INSERT INTO fuel_data SELECT * FROM fuel_df")
    # con.execute("INSERT INTO station_locations SELECT * FROM location_df")

    con.close()
    print("💾 Data stored in db/fuelcheck.duckdb")



if __name__ == "__main__":
    df = pd.read_csv("/Users/bhavyadhingra/Desktop/USYD_Study/SEM_3/Data Engineering/COMP5339_Assignment_1/data/sample.csv")

    store_to_duckdb(df)