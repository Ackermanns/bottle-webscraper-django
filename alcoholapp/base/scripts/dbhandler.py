import sqlite3
import os
     
def create_table_stores(): #GOOD
    """Creates the stores table. This is not expected to be modified"""
    conn = sqlite3.connect('database/booze.db')
    c = conn.cursor()
    query = "CREATE TABLE IF NOT EXISTS stores (store_id INTEGER PRIMARY KEY AUTOINCREMENT, region VARCHAR(30), address VARCHAR(100), phone INTEGER, mail VARCHAR(30), website VARCHAR(100))"
    c.execute(query)
    conn.commit()
    conn.close()

def create_table_item(t_name): #GOOD
    """Creates a new table for a new product that is being sold in stores"""
    conn = sqlite3.connect('database/booze.db')
    c = conn.cursor()
    query = f"CREATE TABLE IF NOT EXISTS {t_name} (store_id INTEGER , entry_id INTEGER PRIMARY KEY, original_price INTEGER, discounted_price INTEGER, litres VARCHAR(15), website VARCHAR(100))"
    c.execute(query)
    conn.commit()
    conn.close()

def commit_queries(filename):
    """Executes all queries from the queries.txt file in the temp folder
       After executing the queries is deleted so when recalled it can start again
    """
    f = open(f"{filename}", "r")
    content = f.readlines()
    conn = sqlite3.connect('database/booze.db')
    c = conn.cursor()
    for query in content:
        try:
            query = query.replace("\n","")
            c.execute(query)
            conn.commit()
        except:
            pass
    conn.close()
'''
def main():
    #commit_queries_tables_table()
    category = 'Liqueurs'
    conn = sqlite3.connect('database/booze.db')
    c = conn.cursor()
    query = f"SELECT table_name, type FROM items WHERE real_name = '{category}';"
    c.execute(query)
    rows = c.fetchall()

    for row in rows:
        print(row)
    
    
    
if __name__ == "__main__":
    main()
'''