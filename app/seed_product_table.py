import os

import psycopg2
from dotenv import load_dotenv


def main() -> None:
    load_dotenv()

    conn = psycopg2.connect(
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT', '5432'),
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
    )
    cur = conn.cursor()
    try:
        # Create product table with a unique constraint on name for idempotent seeding
        cur.execute('''
        CREATE TABLE IF NOT EXISTS product (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL UNIQUE,
            description TEXT,
            price NUMERIC(10, 2) NOT NULL,
            in_stock BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        ''')

        # Insert seed data; skip rows whose name already exists
        cur.execute('''
        INSERT INTO product (name, description, price, in_stock) VALUES
            ('Widget', 'A useful widget', 19.99, TRUE),
            ('Gadget', 'A fancy gadget', 29.99, TRUE),
            ('Thingamajig', 'An interesting thingamajig', 9.99, FALSE)
        ON CONFLICT (name) DO NOTHING;
        ''')

        conn.commit()
        print("Product table created and seeded.")
    finally:
        cur.close()
        conn.close()


if __name__ == "__main__":
    main()
