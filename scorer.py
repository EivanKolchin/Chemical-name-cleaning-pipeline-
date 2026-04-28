import sqlite3 as sql
import pandas as pd 
from rapidfuzz import process
from normaliser import normalise

df = pd.read_csv("queries.csv")
conn = sql.connect("chem_db.db")
cursor = conn.cursor() 

for index, row in df.iterrows():
    query = row["messy_input"]

    print(f"index: {index},\nrow: {row}\n query: {query}")
    
    normalised = normalise(query)
    type, cleaned = normalised['type'], normalised['cleaned']
    candidates = []

    if type == 'iupac_name':
        cursor.execute('SELECT iupac_name FROM compounds')
        all_items = [x[0] for x in cursor.fetchall()]
        best_match = process.extractOne(cleaned, candidates)

        if best_match:
            match_item, score, index = best_match
            print(f"Best match: {match_item}, Score: {score}")
            if score >= 75:
                candidates.append(match_item)

    elif type == 'molecular_formula':

    cursor.execute(f'SELECT iupac_name FROM compounds WHERE {type} = ?', (normalised['cleaned'],))
    candidates = [x[0] for x in cursor.fetchall()]

    for row in candidates:
        print(row)

conn.close()

