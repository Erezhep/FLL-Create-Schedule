from werkzeug.datastructures.file_storage import FileStorage
from pandas.core.frame import DataFrame
from pprint import pprint
import pandas as pd

file = 'teams_fll.xlsx'

def read_excel_file(file: FileStorage):
    
    df = pd.read_excel(file)
    data = get_info_from_excel_file(df)
    
    TEAMS = list(data['Teams'])
    NUM_FIELDS = int(data['Count'][0])
    NUM_ROOMS = int(data['Count'][1])
    BREAK_TIME = int(data['Count'][2])
    
    defense = create_defense_schedule(TEAMS, NUM_ROOMS)
    
    REAL_TIME = 660
    
    day = 1
    
    defenses = {}
    defenses[f"Day - {day}"] = []
    for time, t in defense.items():
        time_to_str = f"{(REAL_TIME - REAL_TIME % 60) // 60:02d}:{REAL_TIME % 60:02d} - {(40 + REAL_TIME - (REAL_TIME + 40) % 60) // 60:02d}:{(REAL_TIME + 40) % 60:02d}"
        defenses[time_to_str] = t
        
        REAL_TIME += 40
        
        if 780 <= REAL_TIME <= 840:
            REAL_TIME = 840
        if REAL_TIME >= 1080:
            day += 1
            defenses[f"Day - {day}"] = []
            REAL_TIME = 600
        
    
    game = create_game_schedule(TEAMS, NUM_FIELDS, defense, BREAK_TIME)
    
    # pprint(NUM_FIELDS)
    
    return {"DEFENSE": defenses, "GAME": game, "NUM_ROOMS": [i for i in range(1, NUM_ROOMS + 1)], "NUM_FIELDS": [j for j in range(1, NUM_FIELDS + 1)]}


def get_info_from_excel_file(df: DataFrame) -> dict:
    
    var = ['Teams', 'Count']
    id = 0
    
    columns = {}
    for col in df.columns:
        if id > 1:
            break
        non_empty_values = df[col].dropna().to_numpy()  # dropna удаляет пустые значения (NaN)
        columns[var[id]] = non_empty_values
        id += 1
    return columns
    
def create_defense_schedule(team: list[str], num_rooms: int) -> dict:
    
    teams = team.copy()
    
    TIME = 40 # Время для защиты каждого команды
    if (len(teams) % num_rooms != 0):
        teams.extend(['' for _ in range(num_rooms - (len(teams) % num_rooms))])
    RESULT = {}
    
    for num in range(1, len(teams) + 1, num_rooms):
        RESULT[TIME] = teams[(num - 1):(num + num_rooms - 1)]
        TIME += 40
    
    return RESULT

def create_game_schedule(team: list[str], num_fields: int, defense_schedule: dict, break_time: int) -> dict:
    
    teams = team.copy()
    
    b_time = break_time - break_time % 10
    MAX_TIME_DEFENSE = max(defense_schedule.keys())
    
    if (len(teams) % num_fields != 0):
        teams.extend(['' for _ in range(num_fields - (len(teams) % num_fields))])
    
    TIME = 10
    time_def = 40
    
    REAL_TIME = 660
    
    day = 1
    days = []
    matches = ['Тренировачная игра', 'Официальная игра 1', 'Официальная игра 2', 'Официальная игра 3']
    RESULT = {}
    for match in matches:
        
        work = teams.copy()[::-1]
        one = {}
        if not day in days:
            one[f"Day - {day}"] = []
            days.append(day)
        while work != []:
            
            if TIME > time_def:
                time_def += 40
            
            update = []
            
            dont_teams = []
            if TIME <= MAX_TIME_DEFENSE:
                dont_teams = defense_schedule[time_def]
                
            res = []
            count = 0
            
            for t in range(1, len(work) + 1):
                if work[-t] not in dont_teams and count < num_fields:
                    res.append(work[-t])
                    count += 1
                else:
                    update.append(work[-t])
            work = update[::-1]
        
            time_to_str = f"{(REAL_TIME - REAL_TIME % 60) // 60:02d}:{REAL_TIME % 60:02d} - {(10 + REAL_TIME - (REAL_TIME + 10) % 60) // 60:02d}:{(REAL_TIME + 10) % 60:02d}"
            one[time_to_str] = res
            
            REAL_TIME += 10
            if 780 <= REAL_TIME <= 840:
                REAL_TIME = 840
            if REAL_TIME >= 1080:
                day += 1
                if not day in days:
                    one[f"Day - {day}"] = []
                    days.append(day)
                REAL_TIME = 600
            
            TIME += 10
        if not (780 <= REAL_TIME <= 840) and REAL_TIME <= 1080 and match != matches[3]:
            one[f"Перерыв на {b_time} мин"] = []
            REAL_TIME += b_time
        RESULT[match] = one
    return RESULT

# if __name__ == "__main__":
#     pprint(read_excel_file(file))