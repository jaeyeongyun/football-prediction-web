# C:\Users\ericy\.gemini\antigravity\scratch\football-prediction-web\database.py

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
                "description": "압도적인 점유율 축구와 홀란드의 가공할 피니시 능력이 조화를 이룹니다."
            },
            "arsenal": {
                "name": "Arsenal",
                "name_kr": "아스널",
                "attack": 2.2,
                "defense": 0.75,
                "elo": 1910,
                "form": ["W", "D", "W", "W", "W"],
                "key_player": "부카요 사카 (Bukayo Saka)",
                "description": "최고 수준의 세트피스 전술과 짜임새 있는 조직력 및 단단한 수비벽을 가졌습니다."
            },
            "liverpool": {
                "name": "Liverpool",
                "name_kr": "리버풀",
                "attack": 2.3,
                "defense": 0.85,
                "elo": 1900,
                "form": ["W", "W", "L", "W", "W"],
                "key_player": "모하메드 살라 (Mohamed Salah)",
                "description": "빠른 템포의 전환 축구와 측면 역습 능력이 매우 위협적입니다."
            },
            "chelsea": {
                "name": "Chelsea",
                "name_kr": "첼시",
                "attack": 1.9,
                "defense": 1.1,
                "elo": 1780,
                "form": ["W", "D", "L", "W", "D"],
                "key_player": "콜 파머 (Cole Palmer)",
                "description": "콜 파머를 기점으로 한 창의적인 공격이 돋보이나 수비 불안 요소가 상존합니다."
            },
            "manunited": {
                "name": "Manchester United",
                "name_kr": "맨체스터 유나이티드",
                "attack": 1.6,
                "defense": 1.2,
                "elo": 1740,
                "form": ["L", "W", "D", "L", "W"],
                "key_player": "브루노 페르난데스 (Bruno Fernandes)",
                "description": "전술적 유연성과 개별 자원의 퀄리티는 우수하나 기복이 심한 편입니다."
            },
            "tottenham": {
                "name": "Tottenham Hotspur",
                "name_kr": "토트넘 홋스퍼",
                "attack": 2.0,
                "defense": 1.3,
                "elo": 1760,
                "form": ["W", "L", "W", "L", "W"],
                "key_player": "손흥민 (Heung-min Son)",
                "description": "공격적인 라인 운영과 빠른 속도의 전환을 선호하나 배후 공간 노출 위험이 큽니다."
            },
            "astonvilla": {
                "name": "Aston Villa",
                "name_kr": "아스톤 빌라",
                "attack": 1.8,
                "defense": 1.1,
                "elo": 1770,
                "form": ["D", "W", "W", "L", "D"],
                "key_player": "올리 왓킨스 (Ollie Watkins)",
                "description": "조직적인 오프사이드 트랩 활용과 날카로운 역습을 구사하는 까다로운 팀입니다."
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
                "description": "월드클래스 선수들의 개인 기량과 챔피언스리그 DNA로 위기 상황에 극도로 강합니다."
            },
            "barcelona": {
                "name": "Barcelona",
                "name_kr": "바르셀로나",
                "attack": 2.4,
                "defense": 0.85,
                "elo": 1900,
                "form": ["W", "L", "W", "W", "W"],
                "key_player": "라민 야말 (Lamine Yamal)",
                "description": "강력한 하이 프레스와 유기적인 패스 앤 무브로 가공할 득점력을 보여줍니다."
            },
            "atletico": {
                "name": "Atletico Madrid",
                "name_kr": "아틀레티코 마드리드",
                "attack": 1.8,
                "defense": 0.78,
                "elo": 1820,
                "form": ["W", "D", "W", "L", "W"],
                "key_player": "앙투안 그리즈만 (Antoine Griezmann)",
                "description": "시메오네 감독 아래 다져진 견고한 두 줄 수비와 그리즈만의 천재성이 돋보입니다."
            },
            "girona": {
                "name": "Girona",
                "name_kr": "지로나",
                "attack": 1.7,
                "defense": 1.2,
                "elo": 1720,
                "form": ["L", "W", "D", "W", "L"],
                "key_player": "빅토르 치한코우 (Viktor Tsygankov)",
                "description": "유기적인 윙백의 오버랩과 유기적인 하프스페이스 공략이 장점입니다."
            },
            "bilbao": {
                "name": "Athletic Bilbao",
                "name_kr": "아틀레틱 빌바오",
                "attack": 1.65,
                "defense": 0.95,
                "elo": 1750,
                "form": ["W", "D", "W", "D", "W"],
                "key_player": "니코 윌리엄스 (Nico Williams)",
                "description": "윌리엄스 형제를 필두로 한 측면 에너지가 매우 뛰어난 팀입니다."
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
                "description": "3-5-2 포메이션의 마스터클래스이며 공수 밸런스가 이탈리아 내 최강입니다."
            },
            "milan": {
                "name": "AC Milan",
                "name_kr": "AC 밀란",
                "attack": 1.85,
                "defense": 1.1,
                "elo": 1790,
                "form": ["W", "L", "W", "W", "D"],
                "key_player": "하파엘 레앙 (Rafael Leao)",
                "description": "레앙의 폭발적인 왼쪽 측면 돌파력을 기반으로 한 다이내믹 공격이 특징입니다."
            },
            "juventus": {
                "name": "Juventus",
                "name_kr": "유벤투스",
                "attack": 1.6,
                "defense": 0.65,
                "elo": 1810,
                "form": ["D", "W", "D", "W", "D"],
                "key_player": "두산 블라호비치 (Dusan Vlahovic)",
                "description": "견고함을 넘어 철벽에 가까운 실점 제어 능력을 보여주는 짠물 축구입니다."
            },
            "napoli": {
                "name": "Napoli",
                "name_kr": "나폴리",
                "attack": 1.75,
                "defense": 0.8,
                "elo": 1800,
                "form": ["W", "W", "L", "W", "W"],
                "key_player": "흐비차 크바라츠헬리아 (Khvicha Kvaratskhelia)",
                "description": "조직적인 블록 수비와 역습 시 빠른 크바라츠헬리아의 결정력을 중시합니다."
            },
            "atalanta": {
                "name": "Atalanta",
                "name_kr": "아탈란타",
                "attack": 2.15,
                "defense": 1.15,
                "elo": 1830,
                "form": ["W", "W", "W", "W", "W"],
                "key_player": "아데몰라 루크먼 (Ademola Lookman)",
                "description": "전방 맨투맨 압박과 폭발적인 전원 공격 성향을 구사해 대량 득점이 잦습니다."
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
                "description": "높은 볼 점유율과 전방 압박, 해리 케인의 완성형 스트라이커 움직임이 결합되었습니다."
            },
            "leverkusen": {
                "name": "Bayer Leverkusen",
                "name_kr": "바이어 레버쿠젠",
                "attack": 2.1,
                "defense": 1.05,
                "elo": 1850,
                "form": ["D", "W", "D", "W", "D"],
                "key_player": "플로리안 비르츠 (Florian Wirtz)",
                "description": "사비 알론소 감독 하에 완성도 높은 후방 빌드업과 비르츠 조율 하에 정교한 패스 축구를 펼칩니다."
            },
            "dortmund": {
                "name": "Borussia Dortmund",
                "name_kr": "보루시아 도르트문트",
                "attack": 1.9,
                "defense": 1.25,
                "elo": 1780,
                "form": ["L", "W", "L", "W", "W"],
                "key_player": "율리안 브란트 (Julian Brandt)",
                "description": "홈 시그널 이두나 파크의 노란 장벽 응원에 힙입어 홈 극강의 위력을 발휘합니다."
            },
            "leipzig": {
                "name": "RB Leipzig",
                "name_kr": "RB 라이프치히",
                "attack": 1.8,
                "defense": 0.9,
                "elo": 1800,
                "form": ["W", "D", "W", "L", "D"],
                "key_player": "로이스 오펜다 (Lois Openda)",
                "description": "레드불 특유의 강렬한 압박 템포와 오펜다의 폭발적인 배후 침투 역습이 위력적입니다."
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
