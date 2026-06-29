import json
import os
import boto3
import pymysql

secrets_client = boto3.client("secretsmanager")

def get_secret():
    secret_name = os.environ["SECRET_NAME"]

    response = secrets_client.get_secret_value(
    SecretId=secret_name
)

    return json.loads(response["SecretString"])


def get_connection():

    secret = get_secret()

    connection = pymysql.connect(
    host=secret["host"],
    user=secret["username"],
    password=secret["password"],
    database="customerdb",
    cursorclass=pymysql.cursors.DictCursor
)

    return connection


def initialize_database(connection):

    try:

        cursor = connection.cursor()

        cursor.execute("""
        SELECT COUNT(*)
        AS table_count
        FROM information_schema.tables
        WHERE table_schema = DATABASE()
        """)

        result = cursor.fetchone()

        if result["table_count"] == 0:

            with open("database_script.sql", "r") as file:

                sql_script = file.read()

        statements = sql_script.split(";")

        for statement in statements:

            if statement.strip():
                cursor.execute(statement)

        connection.commit()

        print("Database initialized successfully")

    except Exception as e:

        print(f"Initialization Error: {str(e)}")

    raise


def get_customer_transaction_details(
connection,
customer_id
):


    cursor = connection.cursor()

    query = """
    SELECT

    c.customer_id,

    COUNT(t.transaction_id)
    AS transaction_count,

    COALESCE(
        SUM(t.amount),
        0
    ) AS total_amount

    FROM Customer c

    JOIN Account a
        ON c.customer_id = a.customer_id

    JOIN TransactionTable t
        ON a.account_id = t.account_id

    WHERE c.customer_id = %s

    GROUP BY c.customer_id
    """

    cursor.execute(query, (customer_id,))

    result = cursor.fetchone()

    return result


def lambda_handler(event, context):


    connection = None

    try:

        headers = event.get("headers", {})

        customer_id = headers.get("customer_id")

        if not customer_id:

            return {
            "statusCode": 400,
            "body": json.dumps(
                {
                    "message":
                    "customer_id header is required"
                }
            )
        }

        connection = get_connection()

        initialize_database(connection)

        result = get_customer_transaction_details(
        connection,
        customer_id
    )

        if not result:

            return {
            "statusCode": 404,
            "headers": {
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps(
                {
                    "message":
                    "Customer not found"
                }
            )
        }

        response = {
        "customer_id":
            result["customer_id"],

        "transaction_count":
            result["transaction_count"],

        "total_amount":
            float(result["total_amount"])
    }

        return {
        "statusCode": 200,

        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "*",
            "Content-Type": "application/json"
        },

        "body": json.dumps(response)
    }

    except Exception as e:

        print(str(e))

        return {
        "statusCode": 500,

        "headers": {
            "Access-Control-Allow-Origin": "*"
        },

        "body": json.dumps(
            {
                "message": "Internal Server Error",
                "error": str(e)
            }
        )
    }

    finally:

        if connection:
            connection.close()

