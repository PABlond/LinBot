import datetime
import os

def get_next_round(round_duration: int):
    next_round = datetime.datetime.now() + datetime.timedelta(seconds=round_duration)
    return str(next_round.time()).split('.')[0]

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')