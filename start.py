import pandas as pd


df = pd.read_csv("data/Valiant 2025 - Looker Studio - Scrim champs.csv")

print(df.columns)

colonnes_a_garder = ['Date', 'Top', 'Jgl', 'Mid', 'Bot', 'Sup', 'Patch', 'Win - Lose',
                      'Opponent', 'E-Top', 'E-Jgl', 'E-Mid', 'E-Bot', 'E-Sup', 'side']

df = df[colonnes_a_garder]

print(df.head())

champion_stats = {'Top': {}, 'Jgl': {}, 'Mid': {}, 'Bot': {}, 'Sup': {}}

for index, row in df.iterrows():
    for role in ['Top', 'Jgl', 'Mid', 'Bot', 'Sup']:
        champion = row[role]
        result = row['Win - Lose']
        
        if champion not in champion_stats[role]:
            champion_stats[role][champion] = {'count': 0, 'wins': 0}
        
        champion_stats[role][champion]['count'] += 1
        if result == 'Win':
            champion_stats[role][champion]['wins'] += 1

winrate_stats = {'Top': [], 'Jgl': [], 'Mid': [], 'Bot': [], 'Sup': []}
total_matches = len(df) 

for role in ['Top', 'Jgl', 'Mid', 'Bot', 'Sup']:
    for champion, stats in champion_stats[role].items():
        winrate = stats['wins'] / stats['count'] if stats['count'] > 0 else 0
        pickrate = stats['count'] / total_matches  
        winrate_stats[role].append({
            'Champion': champion,
            'winrate': round(winrate, 2),
            'pickrate': round(pickrate, 2),
            'count': stats['count'],
            'role': role  
        })

dfs = {}
for role, champions in winrate_stats.items():
    df_role = pd.DataFrame(champions)
    df_role['role'] = role  
    dfs[role] = df_role.nlargest(5, 'count')  

final_df = pd.concat(dfs.values(), ignore_index=True)

final_df = final_df.dropna(subset=['Champion'])

print(final_df)