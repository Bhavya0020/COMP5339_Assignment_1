import duckdb

def test_fuel_data_queries():
    con = duckdb.connect("db/fuelcheck.duckdb")

    # Preview top 5 rows
    print("🧾 Sample rows from fuel_data:")
    df_preview = con.execute("SELECT * FROM fuel_data LIMIT 5").fetchdf()
    print(df_preview)

    # Count total records
    total = con.execute("SELECT COUNT(*) AS total_rows FROM fuel_data").fetchone()[0]
    print(f"\n📊 Total rows in fuel_data: {total}")

    # Example: Get average price per fuel type (replace with your column names if different)
    print("\n⛽ Average price per fuel type:")
    avg_price = con.execute("""
        SELECT source_file, AVG(price) AS avg_price
        FROM fuel_data
        GROUP BY source_file
        ORDER BY avg_price DESC
        LIMIT 10
    """).fetchdf()
    print(avg_price)

    con.close()

if __name__ == "__main__":
    test_fuel_data_queries()
