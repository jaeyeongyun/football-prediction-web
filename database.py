
# 리그별 주요 축구 구단 데이터베이스 (2025-2026 시즌 반영)
# attack: 평균 경기당 득점 계수 (기본값 근처, 높을수록 공격력 강함)
# defense: 평균 경기당 실점 계수 (기본값 근처, 낮을수록 수비력 강함)
# elo: 전력 등급 (1500~2000)
# form: 최근 5경기 결과 (W: 승, D: 무, L: 패)

LEAGUE_DATA = {
    "epl": {
        "name": "English Premier League",
        "name_kr": "잉글리시 프리미어리그",
        "color": "from-purple-600 to-indigo-900",
        "teams": {
            "mancity": {
                "name": "Manchester City",
                "name_kr": "맨체스터 시티",
                "attack": 2.4,
                "defense": 0.8,
                "elo": 1950,
                "form": ["W", "W", "D", "W", "W"],
                "key_player": "엘링 홀란드 (Erling Haaland)",
                "description": "Sustained possession play paired with Haaland's finishing in the box."
            },
            "arsenal": {
                "name": "Arsenal",
                "name_kr": "아스널",
                "attack": 2.2,
                "defense": 0.75,
                "elo": 1910,
                "form": ["W", "D", "W", "W", "W"],
                "key_player": "부카요 사카 (Bukayo Saka)",
                "description": "Elite set-piece routines behind a well-drilled, compact defensive structure."
            },
            "liverpool": {
                "name": "Liverpool",
                "name_kr": "리버풀",
                "attack": 2.3,
                "defense": 0.85,
                "elo": 1900,
                "form": ["W", "W", "L", "W", "W"],
                "key_player": "모하메드 살라 (Mohamed Salah)",
                "description": "Quick transitions and dangerous counter-attacking play down the flanks."
            },
            "chelsea": {
                "name": "Chelsea",
                "name_kr": "첼시",
                "attack": 1.9,
                "defense": 1.1,
                "elo": 1780,
                "form": ["W", "D", "L", "W", "D"],
                "key_player": "콜 파머 (Cole Palmer)",
                "description": "Creative attacking play built around Palmer, offset by defensive lapses."
            },
            "manunited": {
                "name": "Manchester United",
                "name_kr": "맨체스터 유나이티드",
                "attack": 1.6,
                "defense": 1.2,
                "elo": 1740,
                "form": ["L", "W", "D", "L", "W"],
                "key_player": "브루노 페르난데스 (Bruno Fernandes)",
                "description": "Tactically flexible with strong individuals, but inconsistent week to week."
            },
            "tottenham": {
                "name": "Tottenham Hotspur",
                "name_kr": "토트넘 홋스퍼",
                "attack": 2.0,
                "defense": 1.3,
                "elo": 1760,
                "form": ["W", "L", "W", "L", "W"],
                "key_player": "손흥민 (Heung-min Son)",
                "description": "A high defensive line and fast transitions, at the cost of space in behind."
            },
            "astonvilla": {
                "name": "Aston Villa",
                "name_kr": "아스톤 빌라",
                "attack": 1.8,
                "defense": 1.1,
                "elo": 1770,
                "form": ["D", "W", "W", "L", "D"],
                "key_player": "올리 왓킨스 (Ollie Watkins)",
                "description": "A disciplined offside trap and sharp counter-attacks make them awkward to break down."
            }
        }
    },
    "laliga": {
        "name": "La Liga",
        "name_kr": "라리가",
        "color": "from-yellow-500 to-amber-700",
        "teams": {
            "realmadrid": {
                "name": "Real Madrid",
                "name_kr": "레알 마드리드",
                "attack": 2.3,
                "defense": 0.7,
                "elo": 1940,
                "form": ["W", "W", "W", "D", "W"],
                "key_player": "킬리안 음바페 (Kylian Mbappe)",
                "description": "World-class individuals and deep European experience, at their best under pressure."
            },
            "barcelona": {
                "name": "Barcelona",
                "name_kr": "바르셀로나",
                "attack": 2.4,
                "defense": 0.85,
                "elo": 1900,
                "form": ["W", "L", "W", "W", "W"],
                "key_player": "라민 야말 (Lamine Yamal)",
                "description": "An aggressive high press and fluid passing movement generate high-volume chances."
            },
            "atletico": {
                "name": "Atletico Madrid",
                "name_kr": "아틀레티코 마드리드",
                "attack": 1.8,
                "defense": 0.78,
                "elo": 1820,
                "form": ["W", "D", "W", "L", "W"],
                "key_player": "앙투안 그리즈만 (Antoine Griezmann)",
                "description": "A solid two-bank defensive shape under Simeone, with Griezmann providing the spark."
            },
            "girona": {
                "name": "Girona",
                "name_kr": "지로나",
                "attack": 1.7,
                "defense": 1.2,
                "elo": 1720,
                "form": ["L", "W", "D", "W", "L"],
                "key_player": "빅토르 치한코우 (Viktor Tsygankov)",
                "description": "Overlapping wing-backs and consistent attacks through the half-spaces."
            },
            "bilbao": {
                "name": "Athletic Bilbao",
                "name_kr": "아틀레틱 빌바오",
                "attack": 1.65,
                "defense": 0.95,
                "elo": 1750,
                "form": ["W", "D", "W", "D", "W"],
                "key_player": "니코 윌리엄스 (Nico Williams)",
                "description": "Relentless energy out wide, led by the Williams brothers."
            }
        }
    },
    "seriea": {
        "name": "Serie A",
        "name_kr": "세리에 A",
        "color": "from-blue-600 to-cyan-900",
        "teams": {
            "inter": {
                "name": "Inter Milan",
                "name_kr": "인터 밀란",
                "attack": 2.1,
                "defense": 0.7,
                "elo": 1890,
                "form": ["W", "W", "W", "D", "W"],
                "key_player": "라우타로 마르티네스 (Lautaro Martinez)",
                "description": "A masterclass in the 3-5-2, with the best attack-defence balance in Serie A."
            },
            "milan": {
                "name": "AC Milan",
                "name_kr": "AC 밀란",
                "attack": 1.85,
                "defense": 1.1,
                "elo": 1790,
                "form": ["W", "L", "W", "W", "D"],
                "key_player": "하파엘 레앙 (Rafael Leao)",
                "description": "Dynamic attacking play built on Leao's directness down the left."
            },
            "juventus": {
                "name": "Juventus",
                "name_kr": "유벤투스",
                "attack": 1.6,
                "defense": 0.65,
                "elo": 1810,
                "form": ["D", "W", "D", "W", "D"],
                "key_player": "두산 블라호비치 (Dusan Vlahovic)",
                "description": "Miserly at the back, with exceptional control of the chances they concede."
            },
            "napoli": {
                "name": "Napoli",
                "name_kr": "나폴리",
                "attack": 1.75,
                "defense": 0.8,
                "elo": 1800,
                "form": ["W", "W", "L", "W", "W"],
                "key_player": "흐비차 크바라츠헬리아 (Khvicha Kvaratskhelia)",
                "description": "A well-organised defensive block, springing forward through Kvaratskhelia."
            },
            "atalanta": {
                "name": "Atalanta",
                "name_kr": "아탈란타",
                "attack": 2.15,
                "defense": 1.15,
                "elo": 1830,
                "form": ["W", "W", "W", "W", "W"],
                "key_player": "아데몰라 루크먼 (Ademola Lookman)",
                "description": "Man-oriented pressing and all-out attacking commitment produce high-scoring games."
            }
        }
    },
    "bundesliga": {
        "name": "Bundesliga",
        "name_kr": "분데스리가",
        "color": "from-red-600 to-rose-950",
        "teams": {
            "bayern": {
                "name": "Bayern Munich",
                "name_kr": "바이에른 뮌헨",
                "attack": 2.6,
                "defense": 0.8,
                "elo": 1920,
                "form": ["W", "W", "W", "D", "W"],
                "key_player": "해리 케인 (Harry Kane)",
                "description": "High possession and front-foot pressing, finished by Kane's complete centre-forward play."
            },
            "leverkusen": {
                "name": "Bayer Leverkusen",
                "name_kr": "바이어 레버쿠젠",
                "attack": 2.1,
                "defense": 1.05,
                "elo": 1850,
                "form": ["D", "W", "D", "W", "D"],
                "key_player": "플로리안 비르츠 (Florian Wirtz)",
                "description": "Polished build-up under Alonso, with Wirtz orchestrating in the final third."
            },
            "dortmund": {
                "name": "Borussia Dortmund",
                "name_kr": "보루시아 도르트문트",
                "attack": 1.9,
                "defense": 1.25,
                "elo": 1780,
                "form": ["L", "W", "L", "W", "W"],
                "key_player": "율리안 브란트 (Julian Brandt)",
                "description": "Formidable at home, driven by the Yellow Wall at Signal Iduna Park."
            },
            "leipzig": {
                "name": "RB Leipzig",
                "name_kr": "RB 라이프치히",
                "attack": 1.8,
                "defense": 0.9,
                "elo": 1800,
                "form": ["W", "D", "W", "L", "D"],
                "key_player": "로이스 오펜다 (Lois Openda)",
                "description": "The Red Bull pressing template, with Openda attacking space in behind."
            }
        }
    }
}

# 기본 가상Fixture 일정 리스트 (사용자에게 예측을 제안할 대표적 명경기들)
FIXTURE_TEMPLATES = [
    {
        "id": "fix1",
        "league": "epl",
        "home": "mancity",
        "away": "arsenal",
        "date": "2026-05-30",
        "time": "20:30",
        "featured": True
    },
    {
        "id": "fix2",
        "league": "laliga",
        "home": "realmadrid",
        "away": "barcelona",
        "date": "2026-05-31",
        "time": "22:00",
        "featured": True
    },
    {
        "id": "fix3",
        "league": "seriea",
        "home": "inter",
        "away": "juventus",
        "date": "2026-06-01",
        "time": "03:45",
        "featured": False
    },
    {
        "id": "fix4",
        "league": "bundesliga",
        "home": "bayern",
        "away": "leverkusen",
        "date": "2026-06-02",
        "time": "01:30",
        "featured": True
    },
    {
        "id": "fix5",
        "league": "epl",
        "home": "tottenham",
        "away": "liverpool",
        "date": "2026-06-03",
        "time": "04:00",
        "featured": False
    },
    {
        "id": "fix6",
        "league": "seriea",
        "home": "napoli",
        "away": "atalanta",
        "date": "2026-06-04",
        "time": "02:45",
        "featured": False
    }
]
