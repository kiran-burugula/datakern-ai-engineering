import os
import psycopg2

from dotenv import load_dotenv

load_dotenv()

db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASS")

connection = psycopg2.connect(
    host=db_host,
    port=db_port,
    database=db_name,
    user=db_user,
    password=db_password
)

def get_client(client_id):
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            client_id,
            first_name,
            last_name,
            risk_tolerance
        FROM advisory.clients
        WHERE client_id = %s;
        """,
        (client_id,)
    )

    result = cursor.fetchone()

    cursor.close()

    if result is None:
        return None
    else:
        return result

def get_portfolio(client_id):
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            portfolio_id,
            cash_balance,
            total_value
        FROM advisory.portfolios
        WHERE client_id = %s;   
        """,
        (client_id,)
    )

    result = cursor.fetchone()
    
    cursor.close()

    if result is None:
        return None
    else:
        return result

def get_holdings(portfolio_id):
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            ticker,
            shares,
            average_buy_price
        FROM advisory.portfolio_holdings
        WHERE portfolio_id = %s;   
        """,
        (portfolio_id,)
    )

    results = cursor.fetchall()
    
    cursor.close()

    if not results:
        return []
    else:
        return results

def get_client_portfolio(client_id):
    client = get_client(client_id)

    if client is None:
        return None

    client_dict = {
        "client_id": client[0],
        "first_name": client[1],
        "last_name": client[2],
        "risk_tolerance": client[3]
    }

    portfolio = get_portfolio(client_dict["client_id"])

    if portfolio is None:
        return None

    portfolio_dict = {
        "portfolio_id": portfolio[0],
        "cash_balance": portfolio[1],
        "total_value": portfolio[2],
    }

    holdings = get_holdings(portfolio_dict['portfolio_id'])

    holdings_list = []

    for holding in holdings:
        holdings_list.append({
            "ticker": holding[0],
            "shares": holding[1],
            "average_buy_price": holding[2]
        })

    client_portfolio_context = {
        "client": client_dict,
        "portfolio": portfolio_dict,
        "holdings": holdings_list 
    }

    return client_portfolio_context
