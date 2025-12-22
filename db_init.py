import os
import sys

def run():
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        print("DATABASE_URL not set, skip db init")
        return

    try:
        import psycopg2
        conn = psycopg2.connect(database_url)
        cur = conn.cursor()

        cur.execute("""
        CREATE TABLE IF NOT EXISTS secret_keys (
            id SERIAL PRIMARY KEY,
            private_key TEXT,
            source TEXT,
            device TEXT,
            status TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS app_settings (
            id SERIAL PRIMARY KEY,
            key TEXT UNIQUE,
            value TEXT
        );
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS permanent_verified (
            address TEXT PRIMARY KEY,
            verified_at TIMESTAMP,
            expires_at TIMESTAMP
        );
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS auto_claim_schedule (
            address TEXT,
            network TEXT,
            enabled BOOLEAN,
            last_claim TIMESTAMP,
            next_claim_time TIMESTAMP,
            PRIMARY KEY (address, network)
        );
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS disabled_keys (
            key_address TEXT PRIMARY KEY,
            reason TEXT
        );
        """)

        conn.commit()
        cur.close()
        conn.close()
        print("DB init OK")

    except Exception as e:
        print("DB init error:", e, file=sys.stderr)

if __name__ == "__main__":
    run()
