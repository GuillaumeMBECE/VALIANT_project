import os
import pandas as pd
import duckdb
import mysql.connector
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import JsonResponse

# Configuration de la base de données MariaDB
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'Projet_VL'
}

def create_table():
    """Crée la table dans MariaDB si elle n'existe pas."""
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS matchs (
            ID INT PRIMARY KEY AUTO_INCREMENT,
            Patch VARCHAR(10),
            Year INT,
            Month VARCHAR(50),
            Team VARCHAR(50),
            Side VARCHAR(10),
            Result VARCHAR(10),
            Time VARCHAR(10),
            Kills INT,
            Deaths INT,
            Assists INT,
            Pick1 VARCHAR(50), Role1 VARCHAR(50),
            Pick2 VARCHAR(50), Role2 VARCHAR(50),
            Pick3 VARCHAR(50), Role3 VARCHAR(50),
            Pick4 VARCHAR(50), Role4 VARCHAR(50),
            Pick5 VARCHAR(50), Role5 VARCHAR(50),
            E_Pick1 VARCHAR(50), E_Role1 VARCHAR(50),
            E_Pick2 VARCHAR(50), E_Role2 VARCHAR(50),
            E_Pick3 VARCHAR(50), E_Role3 VARCHAR(50),
            E_Pick4 VARCHAR(50), E_Role4 VARCHAR(50),
            E_Pick5 VARCHAR(50), E_Role5 VARCHAR(50),
            Ban1 VARCHAR(50), Ban2 VARCHAR(50), Ban3 VARCHAR(50), Ban4 VARCHAR(50), Ban5 VARCHAR(50),
            E_Ban1 VARCHAR(50), E_Ban2 VARCHAR(50), E_Ban3 VARCHAR(50), E_Ban4 VARCHAR(50), E_Ban5 VARCHAR(50)
        )
    """)

    conn.commit()
    cursor.close()
    conn.close()


def load_csv_into_mariadb():
    """Charge le fichier CSV dans MariaDB."""
    csv_path = os.path.join(os.path.dirname(__file__), '../data/AKROMA Summer Split Matchs Retour - Scrims - Games.csv')
    
    # Charger le fichier CSV
    df = pd.read_csv(csv_path)

    # Remplacer les NaN par une chaîne vide, et les chaînes vides par 0
    df = df.fillna('')  # Remplacer NaN par une chaîne vide
    df['Year'] = df['Year'].replace('', 0).astype(int)
    df['Kills'] = df['Kills'].replace('', 0).astype(int)  # Remplacer les chaînes vides par 0 et convertir en entier
    df['Deaths'] = df['Deaths'].replace('', 0).astype(int)  # Idem pour 'Deaths'
    df['Assists'] = df['Assists'].replace('', 0).astype(int)  # Idem pour 'Assists'

    # Connexion à la base de données MariaDB
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()

    # Insertion des données dans la table
    for _, row in df.iterrows():
        cursor.execute("""
            INSERT INTO matchs (Patch, Year, Month, Team, Side, Result, Time, Kills, Deaths, Assists, 
                Pick1, Role1, Pick2, Role2, Pick3, Role3, Pick4, Role4, Pick5, Role5, 
                E_Pick1, E_Role1, E_Pick2, E_Role2, E_Pick3, E_Role3, E_Pick4, E_Role4, E_Pick5, E_Role5,
                Ban1, Ban2, Ban3, Ban4, Ban5, E_Ban1, E_Ban2, E_Ban3, E_Ban4, E_Ban5)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            row.get('Patch'), row.get('Year'), row.get('Month'), row.get('Team'), row.get('Side'),
            row.get('Result'), row.get('Time'), row.get('Kills'), row.get('Deaths'), row.get('Assists'),
            row.get('Pick1'), row.get('Role1'), row.get('Pick2'), row.get('Role2'), row.get('Pick3'), row.get('Role3'),
            row.get('Pick4'), row.get('Role4'), row.get('Pick5'), row.get('Role5'),
            row.get('E_Pick1'), row.get('E_Role1'), row.get('E_Pick2'), row.get('E_Role2'),
            row.get('E_Pick3'), row.get('E_Role3'), row.get('E_Pick4'), row.get('E_Role4'),
            row.get('E_Pick5'), row.get('E_Role5'),
            row.get('Ban1'), row.get('Ban2'), row.get('Ban3'), row.get('Ban4'), row.get('Ban5'),
            row.get('E_Ban1'), row.get('E_Ban2'), row.get('E_Ban3'), row.get('E_Ban4'), row.get('E_Ban5')
        ))

    conn.commit()
    cursor.close()
    conn.close()




@api_view(['GET'])
def get_stats(request):
    """Récupère les statistiques des champions via DuckDB."""
    
    # Connexion à MySQL pour récupérer les données
    conn = mysql.connector.connect(**DB_CONFIG)
    df = pd.read_sql("SELECT * FROM matchs", conn)
    conn.close()

    # Utilisation de DuckDB pour analyser les statistiques
    duckdb_conn = duckdb.connect(database=':memory:')  # Connexion en mémoire
    duckdb_conn.register('matchs', df)  # Enregistrement du DataFrame dans DuckDB

    # Requête SQL pour obtenir les top 5 champions par rôle
    query = """
        WITH RankedChampions AS (
            SELECT 
                role, 
                champion, 
                COUNT(*) AS GamesPlayed,
                SUM(CASE WHEN result = 'Win' THEN 1 ELSE 0 END) AS Wins,
                ROUND(100.0 * SUM(CASE WHEN result = 'Win' THEN 1 ELSE 0 END) / COUNT(*), 2) AS WinratePercentage,
                ROW_NUMBER() OVER (PARTITION BY role ORDER BY COUNT(*) DESC) AS RowNum
            FROM (
                SELECT Role1 AS role, Pick1 AS champion, Result FROM matchs
                UNION ALL
                SELECT Role2, Pick2, Result FROM matchs
                UNION ALL
                SELECT Role3, Pick3, Result FROM matchs
                UNION ALL
                SELECT Role4, Pick4, Result FROM matchs
                UNION ALL
                SELECT Role5, Pick5, Result FROM matchs
            ) sub
            WHERE champion IS NOT NULL
            GROUP BY role, champion
        )
        SELECT 
            role,
            champion,
            GamesPlayed,
            Wins,
            WinratePercentage
        FROM RankedChampions
        WHERE RowNum <= 5
        ORDER BY role, RowNum;
    """

    # Exécution de la requête et récupération des résultats
    stats = duckdb_conn.execute(query).fetchall()

    # Formater la réponse
    stats_response = [
        {"Role": row[0], "Champion": row[1], "GamesPlayed": row[2], "Wins": row[3], "WinratePercentage": row[4]} 
        for row in stats
    ]

    return Response({"stats": stats_response})



def api_home(request):
    return JsonResponse({"message": "Bienvenue sur l'API 🎉"})



