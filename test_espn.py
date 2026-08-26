
import urllib.request
import json

url = "https://site.api.espn.com/apis/site/v2/sports/soccer/eng.1/scoreboard"

try:
    print("ESPN API 호출 중...")
    req = urllib.request.Request(
        url, 
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    )
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode())
        
        # 리그 정보 출력
        leagues = data.get("leagues", [])
        if leagues:
            print(f"리그명: {leagues[0].get('name')}")
            
        events = data.get("events", [])
        print(f"발견된 매치 수: {len(events)}\n")
        
        for idx, event in enumerate(events[:5]):
            print(f"매치 {idx+1}:")
            print(f"  일시: {event.get('date')}")
            print(f"  상태: {event.get('status', {}).get('type', {}).get('detail')}")
            
            competitors = event.get("competitions", [{}])[0].get("competitors", [])
            for comp in competitors:
                team_name = comp.get("team", {}).get("displayName")
                score = comp.get("score")
                home_away = comp.get("homeAway")
                print(f"  [{home_away}] {team_name}: {score}골")
            print("-" * 30)
            
except Exception as e:
    print(f"오류 발생: {e}")
