import sqlite3


def migrate():
    connection = sqlite3.connect("inbox_agent.db")

    try:
        columns = [
            row[1]
            for row in connection.execute(
                "PRAGMA table_info(emails)"
            )
        ]

        if "labels" not in columns:
            connection.execute("""
                ALTER TABLE emails
                ADD COLUMN labels JSON NOT NULL DEFAULT '[]'
            """)

            print("Added labels column to emails table.")
        else:
            print("Labels column already exists.")

        connection.commit()

    finally:
        connection.close()


if __name__ == "__main__":
    migrate()