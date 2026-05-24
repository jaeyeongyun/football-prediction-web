# ⚽ ANTIGRAVITY Football Prediction Platform (FCP)

> **인공지능 & 통계학 기반 축구 경기 예측 대시보드 및 실시간 시뮬레이션 웹 플랫폼**
> 
> 외부 유료 스포츠 API 종속 없이 포아송 분포(Poisson Distribution) 모델과 10,000회 몬테카를로 시뮬레이션(Monte Carlo Simulation) 기법을 탑재하여 100% 영구 무료 분석 서비스를 제공합니다.

---

## ✨ 핵심 기능 (Features)

1. **🏆 실시간 통계 모델 기반 경기 예측**
   - 유럽 4대 리그(프리미어리그, 라리가, 세리에 A, 분데스리가) 구단들의 실시간 스탯(공격 지수, 수비 견고성) 및 최근 5경기 폼(Form), 최신 Elo 레이팅 연동.
   - 포아송 분포 모델을 이용한 경기 스코어 경우의 수 계산 및 승/무/패 예측 확률 출력.
   - Over/Under 2.5골 및 양 팀 득점 여부(BTTS) 정밀 시각화.

2. **⚙️ 인터랙티브 경기 시뮬레이터 (Monte Carlo Simulator)**
   - 두 팀의 공격력, 수비력, 최근 기세를 직접 슬라이더로 조절하여 가상 전력 설정 가능.
   - 10,000회 경기 몬테카를로 난수 시뮬레이션을 가동하여 예상 스코어 Top 3 및 축적 승률 즉석 도출.

3. **📊 리그별 파워 랭킹 & 상세 전술 해설**
   - 구단별 세부 지표와 최근 전적, 그리고 실제 전술 동향(예: 하이 프레스, 점유율 축구 등)을 제공하는 전력 판독 테이블.

4. **📖 축구 통계학 이론 교육 룸**
   - 포아송 분포, Elo 등급 조정, 몬테카를로 분석 등 본 플랫폼에 적용된 현대 축구 분석 통계 모델 이론 소개.

---

## 🛠️ 기술 스택 (Tech Stack)

- **Backend**: Python 3.x, Flask (RESTful API Web Server)
- **Frontend**: HTML5, Vanilla CSS3 (Neon Dark Theme & Glassmorphism Design System), Modern Vanilla JS
- **Statistical Core**: Poisson Probability Distribution Matrix, Monte Carlo Simulated Algorithms (Knuth Method)

---

## 🚀 로컬 실행 방법 (Quick Start)

### 1. 프로젝트 복제 및 이동
```bash
git clone https://github.com/YOUR_GITHUB_USERNAME/football-prediction-web.git
cd football-prediction-web
```

### 2. 필요한 라이브러리 설치
```bash
pip install Flask
```

### 3. 웹 서버 실행
```bash
python app.py
```
> 구동 완료 후 브라우저에서 **`http://localhost:5000`**으로 접속합니다.

---

## 📂 프로젝트 구조 (Directory Structure)

```text
football-prediction-web/
├── app.py                     # Flask 웹 애플리케이션 엔트리포인트 및 API
├── prediction_engine.py       # 포아송 분포 및 몬테카를로 연산 엔진
├── database.py                # 구단 정보 및 일정 데이터베이스
├── templates/
│   └── index.html             # 메인 SPA 템플릿
├── static/
│   ├── css/
│   │   └── style.css          # Glassmorphic 스타일시트
│   └── js/
│       └── app.js             # API 비동기 연동 및 UI 제어
└── .gitignore                 # 깃 허브 제외 목록 파일
```

---

## 📝 라이선스 (License)

이 프로젝트는 오픈소스이며 자유롭게 수정 및 배포가 가능합니다. ⚽
