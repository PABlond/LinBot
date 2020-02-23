import datetime
import json
import os


def get_next_round(round_duration: int):
    next_round = datetime.datetime.now() + datetime.timedelta(seconds=round_duration)
    return str(next_round.time()).split('.')[0]


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def get_ids():
    with open('profiles_ids.lst', 'r') as f:
        lines = [x.replace('\n', '') for x in f.readlines()]
    return lines


def append_ids(data: str):
    if check_duplicate_ids(data) is True:
        with open('profiles_ids.lst', 'a+') as f:
            f.write("\n{}".format(data))


def update_ids(profile_id: str):
    lines = get_ids()
    with open("profiles_ids.lst", "w") as f:
        for line in lines:
            line = line.replace('\n', '')
            if line != profile_id:
                f.write('{}\n'.format(line))


def check_duplicate_ids(data: str):
    lines = get_ids()
    return not data in lines


def store_request(headers, body):
    with open('request.json', 'w') as f:
        json.dump({
            "headers": dict(headers),
            "body": json.loads(body.decode())
        },
            f, ensure_ascii=False, indent=4)


def get_request():
    with open('request.json') as f:
        data = json.load(f)
    return data


def set_request(profile_id: str):
    req = get_request()
    req['body']['invitee']['com.linkedin.voyager.growth.invitation.InviteeProfile']['profileId'] = profile_id
    return req
