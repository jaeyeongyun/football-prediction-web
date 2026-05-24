# C:\Users\ericy\.gemini\antigravity\scratch\football-prediction-web\live_updater.py

import urllib.request
import json
import os
import time
from database import LEAGUE_DATA

# ESPN API 리그별 매핑 키
ESPN_LEAGUES = {
    "epl": {"id": "eng.1", "name": "EPL"},
    "laliga": {"id": "esp.1", "name": "라리가"},
    "seriea": {"id": "ita.1", "name": "세리에 A"},
    "bundesliga": {"id": "ger.1", "name": "분데스리가"}
}

# 로컬 캐시 설정 (60초 동안 캐싱)
CACHE_FILE = "espn_cache.json"
CACHE_DURATION = 60  # 초 단위

# 한국어 팀명 매핑 테이블
TEAM_NAME_MAP = {
    "manchester city": "mancity", "man city": "mancity", "맨체스터 시티": "mancity",
    "arsenal": "arsenal", "아스널": "arsenal", "아스날": "arsenal",
    "liverpool": "liverpool", "리버풀": "liverpool",
    "chelsea": "chelsea", "첼시": "chelsea",
    "manchester united": "manunited", "man united": "manunited", "맨체스터 유나이티드": "manunited",
    "tottenham hotspur": "tottenham", "tottenham": "tottenham", "토트넘 홋스퍼": "tottenham", "토트넘": "tottenham",
    "aston villa": "astonvilla", "아스톤 빌라": "astonvilla", "아스톤빌라": "astonvilla",
    
    "real madrid": "realmadrid", "레알 마드리드": "realmadrid",
    "barcelona": "barcelona", "바르셀로나": "barcelona",
    "atletico madrid": "atletico", "atlético madrid": "atletico", "아틀레티코 마드리드": "atletico",
    "girona": "girona", "지로나": "girona",
    "athletic club": "bilbao", "athletic bilbao": "bilbao", "아틀레틱 빌바오": "bilbao",
    
    "internazionale": "inter", "inter milan": "inter", "인터 밀란": "inter", "인테르": "inter",
    "ac milan": "milan", "ac밀란": "milan", "AC 밀란": "milan",
    "juventus": "juventus", "유벤투스": "juventus",
    "napoli": "napoli", "나폴리": "napoli",
    "atalanta": "atalanta", "아탈란타": "atalanta",
    
    "bayern munich": "bayern", "bayern münchen": "bayern", "바이에른 뮌헨": "bayern",
    "bayer leverkusen": "leverkusen", "바이어 레버쿠젠": "leverkusen",
    "borussia dortmund": "dortmund", "도르트문트": "dortmund",
    "rb leipzig": "leipzig", "라이프치히": "leipzig"
}

def clean_team_name(name):
    """소문자 공백 제거 등 이름 정규화"""
    return name.lower().strip()

def get_team_key(display_name):
    """ESPN의 팀 이름으로 로컬 database.py의 팀 키값 탐색"""
    cleaned = clean_team_name(display_name)
    # 1. 완전 일치 매핑 확인
    if cleaned in TEAM_NAME_MAP:
        return TEAM_NAME_MAP[cleaned]
    
    # 2. 부분 일치 검색
    for name_str, key in TEAM_NAME_MAP.items():
        if name_str in cleaned or cleaned in name_str:
            return key
            
    return None

def fetch_espn_scoreboard(league_id):
    """ESPN API로부터 특정 리그의 스코어보드 데이터 요청 (urllib 사용)"""
    url = f"https://site.api.espn.com/apis/site/v2/sports/soccer/{league_id}/scoreboard"
    try:
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        )
        with urllib.request.urlopen(req, timeout=5) as response:
            return json.loads(response.read().decode())
    except Exception as e:
        print(f"ESPN API 호출 오류 ({league_id}): {e}")
        return None

def get_realtime_fixtures():
    """모든 주요 리그의 실시간 및 예정된 경기 목록을 수집하여 포맷팅 후 반환"""
    now = time.time()
    
    # 1. 캐시 파일 확인 및 읽기
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                cache_data = json.load(f)
                if now - cache_data.get("timestamp", 0) < CACHE_DURATION:
                    print("로컬 캐시 데이터 반환 (60초 미경과)")
                    return cache_data.get("fixtures", [])
        except Exception as e:
            print("캐시 파일 읽기 오류:", e)
            
    print("ESPN 실시간 크롤링 및 API 갱신 중...")
    all_fixtures = []
    
    for league_key, league_info in ESPN_LEAGUES.items():
        espn_id = league_info["id"]
        scoreboard = fetch_espn_scoreboard(espn_id)
        if not scoreboard:
            continue
            
        events = scoreboard.get("events", [])
        # 각 매치를 폼에 맞춰 가공
        for idx, event in enumerate(events):
            status_obj = event.get("status", {})
            status_type = status_obj.get("type", {})
            
            state = status_type.get("state") # pre, in, post
            detail_time = status_type.get("detail", "Scheduled")
            
            # UTC 시간 -> 단순 날짜/시간 파싱
            utc_date = event.get("date", "") # 2026-05-24T15:00Z
            date_str = "오늘"
            time_str = "경기"
            if len(utc_date) >= 16:
                date_str = utc_date[:10]
                time_str = utc_date[11:16]
                
            competitions = event.get("competitions", [{}])[0]
            competitors = competitions.get("competitors", [])
            
            home_raw = None
            away_raw = None
            for competitor in competitors:
                if competitor.get("homeAway") == "home":
                    home_raw = competitor
                else:
                    away_raw = competitor
                    
            if not home_raw or not away_raw:
                continue
                
            home_name = home_raw.get("team", {}).get("displayName")
            away_name = away_raw.get("team", {}).get("displayName")
            
            home_logo = home_raw.get("team", {}).get("logo", "")
            away_logo = away_raw.get("team", {}).get("logo", "")
            
            home_score = home_raw.get("score", "0")
            away_score = away_raw.get("score", "0")
            
            # 로컬 팀 매핑
            home_key = get_team_key(home_name)
            away_key = get_team_key(away_name)
            
            # 로컬 데이터베이스의 팀 정보 로드
            local_league = LEAGUE_DATA.get(league_key, {})
            local_teams = local_league.get("teams", {})
            
            # 홈팀 정보 바인딩
            if home_key and home_key in local_teams:
                home_elo = local_teams[home_key]["elo"]
                home_form = local_teams[home_key]["form"]
                home_kr = local_teams[home_key]["name_kr"]
            else:
                home_elo = 1650  # 기본값
                home_form = ["W", "D", "L"]
                home_kr = home_name
                
            # 원정팀 정보 바인딩
            if away_key and away_key in local_teams:
                away_elo = local_teams[away_key]["elo"]
                away_form = local_teams[away_key]["form"]
                away_kr = local_teams[away_key]["name_kr"]
            else:
                away_elo = 1650
                away_form = ["W", "D", "L"]
                away_kr = away_name
                
            # 경기 상태 텍스트 커스텀 변환 (한국어)
            status_kr = detail_time
            if state == "pre":
                status_kr = f"{time_str} 예정"
            elif state == "in":
                status_kr = f"🔴 {detail_time} (라이브)"
            elif state == "post":
                status_kr = "경기 종료 (FT)"
                
            all_fixtures.append({
                "id": event.get("id", f"espn_{idx}"),
                "league_key": league_key,
                "league_name": LEAGUE_DATA[league_key]["name_kr"],
                "league_color": LEAGUE_DATA[league_key]["color"],
                "date": date_str,
                "time": time_str,
                "status_text": status_kr,
                "state": state, # pre, in, post
                "featured": idx == 0 and league_key == "epl",
                "home": {
                    "id": home_key or f"custom_{home_name}",
                    "name": home_name,
                    "name_kr": home_kr,
                    "elo": home_elo,
                    "form": home_form,
                    "logo": home_logo,
                    "score": home_score
                },
                "away": {
                    "id": away_key or f"custom_{away_name}",
                    "name": away_name,
                    "name_kr": away_kr,
                    "elo": away_elo,
                    "form": away_form,
                    "logo": away_logo,
                    "score": away_score
                }
            })
            
    # 2. 로컬 캐시 생성
    try:
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump({
                "timestamp": now,
                "fixtures": all_fixtures
            }, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print("캐시 파일 쓰기 실패:", e)
        
    return all_fixtures
