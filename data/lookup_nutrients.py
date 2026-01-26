# lookup_nutrients

import pandas as pd
import sqlite3
import numpy as np
from rapidfuzz import process, fuzz, utils

conn = sqlite3.connect("food_data.db")

def find_match(x):
    cur = conn.cursor()

    choices = pd.read_sql("""
        SELECT description_clean 
        FROM food_table;
    """, conn)["description_clean"].dropna().tolist()
    
    matches = process.extract(x, choices, scorer=fuzz.WRatio, limit=2, processor=utils.default_process)
    
    matches_dict = {}
    score_dict = {}
    for name, score, idx in matches:
        matches_dict[name] = pd.read_sql(f"SELECT penalty FROM food_table WHERE description_clean = ?;", conn, params=(name,))['penalty'].tolist()[0]
        score_dict[name] = score

    best_match = min(matches_dict, key=matches_dict.get)
    score = score_dict[best_match]

    best_match_nutri = pd.read_sql("""
        SELECT description_clean, calories, protein_g, carbs_g, fat_g, fiber_g, sodium_mg 
        FROM food_table 
        WHERE description_clean = ?;
    """, conn, params=(best_match,)).iloc[[0]].iloc[0].tolist()

    best_match_nutri_dict = {
        'description': best_match_nutri[0], 
        'calories': best_match_nutri[1], 
        'protein_g': best_match_nutri[2], 
        'carbs_g': best_match_nutri[3],
        'fat_g': best_match_nutri[4],
        'fiber_g': best_match_nutri[5],
        'sodium_mg': best_match_nutri[6],
        'accuracy_score': score
    }

    return best_match_nutri_dict