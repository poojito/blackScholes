import mysql.connector

def get_connection():
    # localhost:3306
    return mysql.connector.connect(host="localhost", user="root", password="Poojittumm1!", database="black_scholes_db")

def insert_input(stock, strike, rate, vol, time):
    conn = get_connection()
    cursor = conn.cursor()
    query = """
        INSERT INTO BlackScholesInputs (StockPrice, StrikePrice, InterestRate, Volatility, TimeToExpiry)
        VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(query, (stock, strike, rate, vol, time))
    conn.commit()
    last_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return last_id
def insert_output(calc_id, stock_shock, vol_shock, price, is_call):
    conn = get_connection()
    cursor = conn.cursor()
    query = """
        INSERT INTO BlackScholesOutputs (StockPriceShock, VolatilityShock, OptionPrice, IsCall, CalculationId)
        VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(query, (float(stock_shock), float(vol_shock), float(price), int(is_call), int(calc_id)))
    conn.commit()
    cursor.close()
    conn.close()
