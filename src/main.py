import requests
import json
from datetime import datetime
from zoneinfo import ZoneInfo
import time

def main(): 
    base_url = "https://fantasy.premierleague.com/api/bootstrap-static/"
    fixtures_url = "https://fantasy.premierleague.com/api/fixtures/"
    # just need fixtures, events and teams from above
    # and to figure out past/current/future weeks

    base_r = requests.get(base_url)
    fixtures_r = requests.get(fixtures_url)

    if base_r.status_code == 200 and fixtures_r.status_code ==200:
        print("200*2 all good probably")
        base_request_json = base_r.json()
        fixtures_request_json = fixtures_r.json()

        events = base_request_json.get("events",[])
        teams = base_request_json.get("teams",[])
        #print(json.dumps(fixtures_request_json,indent=2))

        #look up name via code:
        code_to_name = {t["id"]: t["name"] for t in teams}

        #eg:
        #print(code_to_name.get(3))

        #sort events (game weeks):
        #open a file to save to:
        with open('output.txt','w') as output_file:
            print(f"Last run started : {datetime.fromtimestamp(time.time()).strftime('%d %b %Y %H:%M:%S')}\n",file=output_file)
            for e in events:
                week_state = ""
                if e.get("is_current") == 1:
                    week_state = "This week"
                elif e.get("is_next") == 1: 
                    week_state = "Next week"
                elif e.get("is_previous"):
                    week_state = "Last week"   
                elif e.get("finished") == 1:
                    week_state = "Past week"
                else: 
                    week_state = "Future week"

                #date stuff
                deadline_iso_date = e.get('deadline_time')
                deadline_dt = datetime.fromisoformat(deadline_iso_date.replace('Z','+00:00'))
                uk_deadline = deadline_dt.astimezone(ZoneInfo('Europe/London'))
                deadline_time = uk_deadline.strftime('%d %b %Y %H:%M')

                print(f"{week_state}: {e.get('name')}, Deadline: {deadline_time} ",file=output_file)
                event_fixtures = [f for f in fixtures_request_json if f.get("event") == e.get('id')]
                for fixture in event_fixtures:
                    home_team = code_to_name.get(fixture['team_h'])
                    away_team = code_to_name.get(fixture['team_a'])
                    score = ""
                    iso_date = fixture['kickoff_time']
                    dt = datetime.fromisoformat(iso_date.replace('Z', '+00:00'))
                    uk_date = dt.astimezone(ZoneInfo('Europe/London'))
                    formatted_date = uk_date.strftime("%a") + " " + str (uk_date.day) + get_ordinal_suffix(uk_date.day) + uk_date.strftime(" %b %H:%M")
                    if fixture['started'] == 1:
                        score = f" ({fixture['team_h_score']}-{fixture['team_a_score']})"
                    print(f"{formatted_date} {home_team} VS {away_team}{score}",file=output_file)
                print("",file=output_file)#white space for a line
            print(f"Last run ended : {datetime.fromtimestamp(time.time()).strftime('%d %b %Y %H:%M:%S')}\n",file=output_file)

            

    else:
        print(f"base request returned status : {base_r.status_code}")
        print(f"fixtures request returned status : {fixtures_r.status_code}")
        return

def get_ordinal_suffix(day):
    if 10 <= day % 100 <= 20:
        suffix = 'th'
    else:
        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(day % 10, 'th')
    return suffix

main()



#garbage dump:
        #print("Events: ", len(events))
        #print("Teams: ", len(teams))
        # with open("output.json","w",encoding="utf-8") as f:
        #     json.dump(base_request_json,f,ensure_ascii=False,indent=2)
        #print(teams_simplified)