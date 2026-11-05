import os
from dotenv import load_dotenv
from sqlalchemy import create_engine,text
import psycopg2
load_dotenv()

engine = create_engine(
    f"postgresql+psycopg2://{os.getenv('USER')}:{os.getenv('PASSWORD')}@{os.getenv('HOST')}:{os.getenv('HOST_PORT')}/{os.getenv('DATA_BASE')}"
)

CSV_DIR = "data"

print("Database connection established successfully.")

create_table_query = """
                        CREATE SCHEMA IF NOT EXISTS dagent;
-------------------------------
-- USER------------------------
-------------------------------
CREATE TABLE IF NOT EXISTS dagent.users (
    user_id INTEGER PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    phone VARCHAR(20),
    city VARCHAR(100),
    province VARCHAR(100),
    user_type VARCHAR(50) NOT NULL,
    signup_date DATE,
    is_active BOOLEAN
);


-----------------------------------
-- VECHICLES-----------------------
-----------------------------------
CREATE TABLE IF NOT EXISTS dagent.vehicles (
    vehicle_id INTEGER PRIMARY KEY,
    driver_id INTEGER NOT NULL,
    make VARCHAR(100),
    model VARCHAR(100),
    year INTEGER,
    license_plate VARCHAR(20) UNIQUE,
    color VARCHAR(50),
    is_active BOOLEAN,
    CONSTRAINT fk_driver FOREIGN KEY (driver_id) REFERENCES dagent.users(user_id)
);

--------------------------------
-- RIDES------------------------
--------------------------------

CREATE TABLE IF NOT EXISTS dagent.rides (
    ride_id INTEGER PRIMARY KEY,
    rider_id INTEGER NOT NULL,
    driver_id INTEGER NOT NULL,
    requested_at TIMESTAMP,
    pickup_time TIMESTAMP,
    dropoff_time TIMESTAMP,
    pickup_latitude DECIMAL(9, 6),
    pickup_longitude DECIMAL(9, 6),
    dropoff_latitude DECIMAL(9, 6),
    dropoff_longitude DECIMAL(9, 6),
    distance_km DECIMAL(10, 2),
    fare DECIMAL(10, 2),
    surge_multiplier DECIMAL(3, 2),
    status VARCHAR(50),
    cancellation_reason VARCHAR(255),
    CONSTRAINT fk_rider FOREIGN KEY (rider_id) REFERENCES dagent.users(user_id),
    CONSTRAINT fk_driver FOREIGN KEY (driver_id) REFERENCES dagent.users(user_id)
);

--------------------------------
-- PAYMENTS---------------------
--------------------------------

CREATE TABLE IF NOT EXISTS dagent.payments (
    payment_id INTEGER PRIMARY KEY,
    ride_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    amount DECIMAL(10, 2),
    payment_method VARCHAR(50),
    payment_status VARCHAR(50),
    transaction_id VARCHAR(100) UNIQUE,
    payment_time TIMESTAMP,
    CONSTRAINT fk_ride FOREIGN KEY (ride_id) REFERENCES dagent.rides(ride_id),
    CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES dagent.users(user_id)
);

--------------------------------
-- RATING-----------------------
--------------------------------
CREATE TABLE IF NOT EXISTS dagent.ratings (
    rating_id INTEGER PRIMARY KEY,
    ride_id INTEGER NOT NULL,
    rider_id INTEGER NOT NULL,
    driver_id INTEGER NOT NULL,
    rating DECIMAL(2, 1),
    comment TEXT,
    rated_at TIMESTAMP,
    CONSTRAINT fk_ride FOREIGN KEY (ride_id) REFERENCES dagent.rides(ride_id),
    CONSTRAINT fk_rider FOREIGN KEY (rider_id) REFERENCES dagent.users(user_id),
    CONSTRAINT fk_driver FOREIGN KEY (driver_id) REFERENCES dagent.users(user_id),
    CONSTRAINT chk_rating CHECK (rating >= 1 AND rating <= 5)
);

--------------------------------
--==-- INDEXES------------------
--------------------------------
CREATE INDEX IF NOT EXISTS idx_vehicles_driver_id
ON dagent.vehicles(driver_id);

CREATE INDEX IF NOT EXISTS idx_rides_rider_id
ON dagent.rides(rider_id);

CREATE INDEX IF NOT EXISTS idx_rides_driver_id
ON dagent.rides(driver_id);

CREATE INDEX IF NOT EXISTS idx_rides_requested_at
ON dagent.rides(requested_at);

CREATE INDEX IF NOT EXISTS idx_rides_status
ON dagent.rides(status);

CREATE INDEX IF NOT EXISTS idx_payments_ride_id
ON dagent.payments(ride_id);

CREATE INDEX IF NOT EXISTS idx_payments_user_id
ON dagent.payments(user_id);

CREATE INDEX IF NOT EXISTS idx_ratings_ride_id
ON dagent.ratings(ride_id);

CREATE INDEX IF NOT EXISTS idx_ratings_driver_id
ON dagent.ratings(driver_id);

"""

with engine.begin() as connection:
    connection.execute(text(create_table_query))
print("Tables created successfully in the database.")


def load_csv_to_db(csv_file, table_name, columns):
    csv_path = os.path.join(CSV_DIR, csv_file)
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"CSV file '{csv_path}' not found.")
    copy_sql = (
        f"COPY {table_name} ({', '.join(columns)}) "
        f"FROM STDIN WITH (FORMAT CSV, HEADER TRUE, NULL '')"
    )

    raw = engine.raw_connection()
    try:
        cur = raw.cursor()
          # adding Records count to the table
          
        with open(csv_path, "r", encoding="utf-8") as f:
            cur.copy_expert(copy_sql, f)
        raw.commit()
    except Exception:
        raw.rollback()
        raise
    finally:
        raw.close()

    print(f"Loaded {csv_file} → {table_name}")

# load CSV files into the database
#LOAD USERS 
load_csv_to_db("users.csv", "dagent.users", ["user_id", "first_name", "last_name", "email", "phone", "city", "province", "user_type", "signup_date", "is_active"])
#LOAD VEHICLES
load_csv_to_db("vehicles.csv", "dagent.vehicles", ["vehicle_id", "driver_id", "make", "model", "year", "license_plate", "color", "is_active"])
#LOAD RIDES
load_csv_to_db("rides.csv", "dagent.rides", ["ride_id", "rider_id", "driver_id", "requested_at", "pickup_time", "dropoff_time", "pickup_latitude", "pickup_longitude", "dropoff_latitude", "dropoff_longitude", "distance_km", "fare", "surge_multiplier", "status", "cancellation_reason"])
#LOAD PAYMENTS
load_csv_to_db("payments.csv", "dagent.payments", ["payment_id", "ride_id", "user_id", "amount", "payment_method", "payment_status", "transaction_id", "payment_time"])
#LOAD RATINGS
load_csv_to_db("ratings.csv", "dagent.ratings", ["rating_id", "ride_id", "rider_id", "driver_id", "rating", "comment", "rated_at"])

print("All CSV files loaded successfully into the database.")
