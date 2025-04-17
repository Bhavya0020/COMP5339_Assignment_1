import duckdb
import pandas as pd
pd.set_option('display.max_columns', 20)

def test_fuel_data_queries():
    con = duckdb.connect("db/fuelcheck.duckdb")

    # Show all rows from fuel_data (or limited if necessary)
    print("🧾 All rows from fuel_data:")
    df_all_data = con.execute("SELECT * FROM fuel_data").fetchdf()
    print(df_all_data)

    # Count total records
    total = con.execute("SELECT COUNT(*) AS total_rows FROM fuel_data").fetchone()[0]
    print(f"\n📊 Total rows in fuel_data: {total}")

    # Example: Get average price per fuel type
    print("\n⛽ Average price per fuel type:")
    avg_price = con.execute(
        """
        SELECT fuelcode, AVG(price) AS avg_price
        FROM fuel_data
        GROUP BY fuelcode
        ORDER BY avg_price DESC
        LIMIT 10
    """
    ).fetchdf()
    print(avg_price)

    con.close()

if __name__ == "__main__":
    test_fuel_data_queries()
