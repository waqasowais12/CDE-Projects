import pandas as pd
import pyodbc

# 1️⃣ Load CSV
df = pd.read_csv('cleaned_car_data.csv')

# 2️⃣ SQL Server connection details
server = 'DESKTOP-H96K80L'  # e.g., 'localhost\SQLEXPRESS'
database = 'CarDataDB'
# Connection string
conn = pyodbc.connect(
    f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database}'
)
cursor = conn.cursor()

# 3️⃣ Table create karna (agar table pehle nahi bana hai)
create_table_query = """
IF OBJECT_ID('dbo.Cars', 'U') IS NOT NULL
    DROP TABLE dbo.Cars;

CREATE TABLE dbo.Cars (
    title NVARCHAR(255),
    price FLOAT,
    year INT,
    mileage FLOAT,
    fuel NVARCHAR(50),
    engine FLOAT,
    transmission NVARCHAR(50),
)
"""
cursor.execute(create_table_query)
conn.commit()

# 4️⃣ Insert data row by row
for index, row in df.iterrows():
    cursor.execute("""
        INSERT INTO dbo.Cars (title, price, year, mileage, fuel, engine, transmission)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, row['title'], row['price'], row['year'], row['mileage'], row['fuel'], row['engine'], row['transmission'])

conn.commit()
cursor.close()
conn.close()

print("Data successfully inserted into SQL Server!")
