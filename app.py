
import os
from flask import Flask, jsonify, render_template, request
from database import LEAGUE_DATA
from prediction_engine import generate_prediction, run_monte_carlo, english_player
from live_updater import get_realtime_fixtures

app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static"
)

# 기본 라우트: 메인 대시보드 인덱스 페이지 서빙
@app.route("/")
def index():
    return render_template("index.html")

# API: 전체 리그 및 하위 팀 정보 반환
@app.route("/api/leagues", methods=["GET"])
def get_leagues():
    return jsonify(LEAGUE_DATA)

# API: 실시간 및 예정된 매치 목록 반환 (ESPN API 및 캐시 연동)
@app.route("/api/fixtures", methods=["GET"])
def get_fixtures():
    try:
        # 실시간 크롤링/API 데이터를 로컬 캐시와 연동하여 호출
        resolved_fixtures = get_realtime_fixtures()
        return jsonify(resolved_fixtures)
    except Exception as e:
        print("실시간 경기 수집 실패:", e)
        return jsonify({"error": f"실시간 경기 데이터를 수집할 수 없습니다: {e}"}), 500

# API: 두 특정 팀 대결 예측 수행
@app.route("/api/predict", methods=["GET"])
def predict_match():
    league_key = request.args.get("league")
    home_key = request.args.get("home")
    away_key = request.args.get("away")
    
    if not league_key or not home_key or not away_key:
        return jsonify({"error": "league, home, away 파라미터가 모두 필요합니다."}), 400
        
    league = LEAGUE_DATA.get(league_key)
    if not league:
        return jsonify({"error": "존재하지 않는 리그입니다."}), 404
        
    # 홈팀 객체 생성 (로컬 데이터베이스 매핑 또는 동적 생성)
    if home_key.startswith("custom_"):
        raw_name = home_key.replace("custom_", "")
        home_team = {
            "name": raw_name,
            "name_kr": raw_name,
            "attack": 1.4,
            "defense": 1.25,
            "elo": 1650,
            "form": ["W", "D", "L"],
            "key_player": "에이스 선수 (Ace Player)",
            "description": "최근 전적에 기반해 역동적인 시뮬레이션 전술을 펼치는 팀입니다."
        }
    else:
        home_team = league["teams"].get(home_key)
        
    # 원정팀 객체 생성 (로컬 데이터베이스 매핑 또는 동적 생성)
    if away_key.startswith("custom_"):
        raw_name = away_key.replace("custom_", "")
        away_team = {
            "name": raw_name,
            "name_kr": raw_name,
            "attack": 1.4,
            "defense": 1.25,
            "elo": 1650,
            "form": ["W", "D", "L"],
            "key_player": "에이스 선수 (Ace Player)",
            "description": "최근 전적에 기반해 역동적인 시뮬레이션 전술을 펼치는 팀입니다."
        }
    else:
        away_team = league["teams"].get(away_key)
        
    if not home_team or not away_team:
        return jsonify({"error": "존재하지 않는 팀 매칭입니다."}), 404
        
    # 예측 수행
    prediction = generate_prediction(home_team, away_team, league_key)
    
    # UI 친화적인 디자인을 위한 오리지널 팀 세부정보 주입
    prediction["home_details"] = {
        "elo": home_team["elo"],
        "form": home_team["form"],
        "key_player": english_player(home_team["key_player"]),
        "description": home_team["description"]
    }
    prediction["away_details"] = {
        "elo": away_team["elo"],
        "form": away_team["form"],
        "key_player": english_player(away_team["key_player"]),
        "description": away_team["description"]
    }
    
    return jsonify(prediction)

# API: 커스텀 전력 세부 조절 기반 몬테카를로 시뮬레이션
def _clamp_stats(stats):
    """슬라이더 범위(0~100)를 벗어난 값으로 시뮬레이션이 폭주하지 않도록 제한한다."""
    def num(key, default):
        try:
            value = float(stats.get(key, default))
        except (TypeError, ValueError):
            value = default
        return min(max(value, 0.0), 100.0)

    return {
        "attack": num("attack", 50),
        "defense": num("defense", 50),
        "form": num("form", 50),
        "home_advantage": bool(stats.get("home_advantage", True)),
    }


@app.route("/api/simulate", methods=["POST"])
def simulate_match():
    data = request.get_json()
    if not data or "home" not in data or "away" not in data:
        return jsonify({"error": "home과 away의 능력치 데이터가 필요합니다."}), 400
        
    home_stats = _clamp_stats(data["home"])
    away_stats = _clamp_stats(data["away"])
    
    # 몬테카를로 엔진 구동
    sim_result = run_monte_carlo(home_stats, away_stats)
    return jsonify(sim_result)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
