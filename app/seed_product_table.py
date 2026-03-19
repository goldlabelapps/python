import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()

# Database connection
conn = psycopg2.connect(
    host=os.getenv('DB_HOST'),
    port=os.getenv('DB_PORT', '5432'),
    dbname=os.getenv('DB_NAME'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD')
)
cur = conn.cursor()

# Create product table
cur.execute('''
CREATE TABLE IF NOT EXISTS product (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    price NUMERIC(10, 2) NOT NULL,
    in_stock BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
''')

# Insert seed data
cur.execute('''
INSERT INTO product (name, description, price, in_stock) VALUES
    ('Widget', 'A useful widget', 19.99, TRUE),
    ('Gadget', 'A fancy gadget', 29.99, TRUE),
    ('Thingamajig', 'An interesting thingamajig', 9.99, FALSE)
ON CONFLICT DO NOTHING;
''')

conn.commit()
cur.close()
conn.close()
print("Product table created and seeded.")
