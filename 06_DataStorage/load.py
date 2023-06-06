import time
import psycopg2
import argparse
import csv

DATABASE_NAME = "postgres"
DATABASE_USER = "postgres"
DATABASE_PASSWORD = "admin"
TABLE_NAME = 'Temp'
FILE_NAME = "oregon2015.csv"
SHOULD_CREATE_TABLE = False

def format_row(row):
    for key in row:
        if not row[key]:
            row[key] = 0
        row['County'] = row['County'].replace('\'','')

    formatted_values = ", ".join([f"'{val}'" if isinstance(val, str) else str(val) for val in row.values()])
    return formatted_values


def setup_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", required=True)
    parser.add_argument("-t", "--table", action="store_true")
    args = parser.parse_args()

    global FILE_NAME
    FILE_NAME = args.file
    global SHOULD_CREATE_TABLE
    SHOULD_CREATE_TABLE = args.table


def read_csv_file(file):
    print(f"Reading data from {file}")
    with open(file, mode="r") as f:
        reader = csv.DictReader(f)
        rows = [row for row in reader]
    return rows


def generate_sql_commands(rows):
    command_list = []
    for row in rows:
        formatted_row = format_row(row)
        command = f"INSERT INTO {TABLE_NAME} VALUES ({formatted_row});"
        command_list.append(command)
    return command_list


def connect_to_db():
    connection = psycopg2.connect(
        host="localhost",
        database=DATABASE_NAME,
        user=DATABASE_USER,
        password=DATABASE_PASSWORD,
    )
    connection.autocommit = False
    return connection


def generate_table(connection):
    with connection.cursor() as cursor:
        cursor.execute(f"""
            DROP TABLE IF EXISTS {TABLE_NAME};
            CREATE TABLE {TABLE_NAME} (
                CensusTract         NUMERIC,
                State               TEXT,
                County              TEXT,
                TotalPop            INTEGER,
                Men                 INTEGER,
                Women               INTEGER,
                Hispanic            DECIMAL,
                White               DECIMAL,
                Black               DECIMAL,
                Native              DECIMAL,
                Asian               DECIMAL,
                Pacific             DECIMAL,
                Citizen             DECIMAL,
                Income              DECIMAL,
                IncomeErr           DECIMAL,
                IncomePerCap        DECIMAL,
                IncomePerCapErr     DECIMAL,
                Poverty             DECIMAL,
                ChildPoverty        DECIMAL,
                Professional        DECIMAL,
                Service             DECIMAL,
                Office              DECIMAL,
                Construction        DECIMAL,
                Production          DECIMAL,
                Drive               DECIMAL,
                Carpool             DECIMAL,
                Transit             DECIMAL,
                Walk                DECIMAL,
                OtherTransp         DECIMAL,
                WorkAtHome          DECIMAL,
                MeanCommute         DECIMAL,
                Employed            INTEGER,
                PrivateWork         DECIMAL,
                PublicWork          DECIMAL,
                SelfEmployed        DECIMAL,
                FamilyWork          DECIMAL,
                Unemployment        DECIMAL
            );    
        """)
        print(f"Created {TABLE_NAME}")


def insert_into_db(connection, commands):
    with connection.cursor() as cursor:
        print(f"Inserting {len(commands)} rows")
        start_time = time.perf_counter()
    
        for cmd in commands:
            cursor.execute(cmd)

        elapsed_time = time.perf_counter() - start_time
        print(f'Finished insertion. Elapsed Time: {elapsed_time:.4f} seconds')


def run():
    setup_args()
    conn = connect_to_db()
    rows = read_csv_file(FILE_NAME)
    command_list = generate_sql_commands(rows)

    if SHOULD_CREATE_TABLE:
        generate_table(conn)

    insert_into_db(conn, command_list)


if __name__ == "__main__":
    run()

