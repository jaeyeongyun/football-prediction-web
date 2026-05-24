// C:\Users\ericy\.gemini\antigravity\scratch\football-prediction-web\static\js\app.js

document.addEventListener("DOMContentLoaded", () => {
    // 글로벌 데이터 캐시
    let cachedLeagues = null;

    // DOM 요소 캐시
    const fixturesGrid = document.getElementById("fixtures-grid");
    const standingsBody = document.getElementById("standings-body");
    const leagueTabBtns = document.querySelectorAll(".league-tab-btn");
    
    // 시뮬레이터 요소
    const btnSimulate = document.getElementById("btn-run-simulation");
    const simResultBox = document.getElementById("sim-result-box");
    const homeAttSlider = document.getElementById("sim-home-attack");
    const homeDefSlider = document.getElementById("sim-home-defense");
    const homeFormSlider = document.getElementById("sim-home-form");
    const homeAdvCheck = document.getElementById("sim-home-adv");
    
    const awayAttSlider = document.getElementById("sim-away-attack");
    const awayDefSlider = document.getElementById("sim-away-defense");
    const awayFormSlider = document.getElementById("sim-away-form");
    
    // 시뮬레이터 수치 인디케이터
    const homeAttVal = document.getElementById("home-att-val");
    const homeDefVal = document.getElementById("home-def-val");
    const homeFormVal = document.getElementById("home-form-val");
    const awayAttVal = document.getElementById("away-att-val");
    const awayDefVal = document.getElementById("away-def-val");
    const awayFormVal = document.getElementById("away-form-val");

    // 모달 요소
    const predictModal = document.getElementById("predict-modal");
    const modalCloseBtn = document.getElementById("modal-close-btn");
    const modalCloseFooterBtn = document.getElementById("modal-close-footer-btn");

    /* ----------------------------------------------------
       1. 초기 구동 및 슬라이더 연동
       ---------------------------------------------------- */
    // 슬라이더 값 변경 시 실시간 라벨 업데이트 로직
    const setupSlider = (slider, indicator) => {
        slider.addEventListener("input", (e) => {
            indicator.textContent = e.target.value;
        });
    };
    setupSlider(homeAttSlider, homeAttVal);
    setupSlider(homeDefSlider, homeDefVal);
    setupSlider(homeFormSlider, homeFormVal);
    setupSlider(awayAttSlider, awayAttVal);
    setupSlider(awayDefSlider, awayDefVal);
    setupSlider(awayFormSlider, awayFormVal);

    // 초기 데이터 로딩 호출
    loadFixtures();
    loadLeaguesAndStandings();

    /* ----------------------------------------------------
       2. API 통신 및 데이터 렌더링
       ---------------------------------------------------- */
    // 추천 예정 매치업 목록 가져오기
    function loadFixtures() {
        fetch("/api/fixtures")
            .then(res => res.json())
            .then(fixtures => {
                fixturesGrid.innerHTML = "";
                if (fixtures.length === 0) {
                    fixturesGrid.innerHTML = "<p class='neutral-text'>현재 진행 중이거나 대기 중인 리그 매치업이 없습니다.</p>";
                    return;
                }
                
                fixtures.forEach(fix => {
                    const card = document.createElement("div");
                    card.className = `fixture-card ${fix.featured ? 'featured' : ''} ${fix.state === 'in' ? 'live-border' : ''}`;
                    
                    // 홈/원정 로고 렌더링 (ESPN URL 또는 이니셜 텍스트Fallback)
                    const homeLogoHtml = fix.home.logo 
                        ? `<img src="${fix.home.logo}" class="team-logo-img" alt="${fix.home.name_kr}">` 
                        : `<div class="team-avatar">${fix.home.name_kr[0]}</div>`;
                        
                    const awayLogoHtml = fix.away.logo 
                        ? `<img src="${fix.away.logo}" class="team-logo-img" alt="${fix.away.name_kr}">` 
                        : `<div class="team-avatar">${fix.away.name_kr[0]}</div>`;
                    
                    // 실시간 스코어보드 또는 VS 상태 뱃지
                    let vsHtml = `<div class="vs-badge">VS</div>`;
                    if (fix.state === 'in' || fix.state === 'post') {
                        const pulseClass = fix.state === 'in' ? 'pulse-score' : '';
                        vsHtml = `
                            <div class="vs-badge score-display ${pulseClass}">
                                <span class="score-num">${fix.home.score}</span>
                                <span class="score-dash">-</span>
                                <span class="score-num">${fix.away.score}</span>
                            </div>
                        `;
                    }

                    // 매치 상태별 시간 태그 스타일링
                    const tagClass = fix.state === 'in' ? 'tag-live-pulsing' : (fix.state === 'post' ? 'tag-finished' : '');

                    card.innerHTML = `
                        <div class="card-top">
                            <span class="league-badge" style="background: linear-gradient(135deg, rgba(255,255,255,0.1), rgba(255,255,255,0.05)); border: 1px solid rgba(255,255,255,0.15);">${fix.league_name}</span>
                            <span class="match-time-tag ${tagClass}">${fix.status_text}</span>
                        </div>
                        <div class="match-teams-row">
                            <div class="team-block">
                                <div class="logo-wrapper">${homeLogoHtml}</div>
                                <div class="team-name">${fix.home.name_kr}</div>
                                <div class="team-stat-sub">Elo: ${fix.home.elo}</div>
                            </div>
                            ${vsHtml}
                            <div class="team-block">
                                <div class="logo-wrapper">${awayLogoHtml}</div>
                                <div class="team-name">${fix.away.name_kr}</div>
                                <div class="team-stat-sub">Elo: ${fix.away.elo}</div>
                            </div>
                        </div>
                        <div class="card-action">
                            <div class="form-dots">
                                ${fix.home.form.slice(-3).map(f => `<span class="form-dot ${f.toLowerCase()}" title="홈팀 최근 폼: ${f}"></span>`).join("")}
                                <span style="font-size:0.7rem; color:var(--text-muted); padding:0 3px;">vs</span>
                                ${fix.away.form.slice(-3).map(f => `<span class="form-dot ${f.toLowerCase()}" title="원정팀 최근 폼: ${f}"></span>`).join("")}
                            </div>
                            <a class="btn-predict-link">정밀 분석 & 예측 &rarr;</a>
                        </div>
                    `;
                    
                    // 카드 클릭 시 모달 오픈 및 예측 계산 요청
                    card.addEventListener("click", () => {
                        openPredictionModal(fix.league_key, fix.home.id, fix.away.id);
                    });
                    
                    fixturesGrid.appendChild(card);
                });
            })
            .catch(err => {
                console.error("Fixture 로딩 실패:", err);
                fixturesGrid.innerHTML = "<p class='neutral-text'>⚠️ 예정된 실시간 경기 일정을 가져오는데 실패했습니다.</p>";
            });
    }

    // 리그 테이블 정보 초기화 및 탭 클릭 바인딩
    function loadLeaguesAndStandings() {
        fetch("/api/leagues")
            .then(res => res.json())
            .then(data => {
                cachedLeagues = data;
                // 디폴트로 첫 번째 활성화된 탭(EPL) 렌더링
                renderStandings("epl");
            })
            .catch(err => {
                console.error("League 로딩 실패:", err);
                standingsBody.innerHTML = "<tr><td colspan='5' class='neutral-text'>⚠️ 리그 전력 정보를 가져오는데 실패했습니다.</td></tr>";
            });

        // 탭 버튼 클릭 이벤트 바인딩
        leagueTabBtns.forEach(btn => {
            btn.addEventListener("click", () => {
                leagueTabBtns.forEach(b => b.classList.remove("active"));
                btn.classList.add("active");
                const leagueKey = btn.getAttribute("data-league");
                renderStandings(leagueKey);
            });
        });
    }

    // 파워 랭킹 테이블 렌더링
    function renderStandings(leagueKey) {
        if (!cachedLeagues || !cachedLeagues[leagueKey]) return;
        
        const league = cachedLeagues[leagueKey];
        const teams = league.teams;
        standingsBody.innerHTML = "";
        
        // Elo 스코어 역순(강한 순)으로 구단 정렬
        const sortedTeams = Object.keys(teams).map(key => ({
            id: key,
            ...teams[key]
        })).sort((a, b) => b.elo - a.elo);
        
        sortedTeams.forEach(team => {
            const tr = document.createElement("tr");
            tr.innerHTML = `
                <td>
                    <div class="team-info-cell">
                        <div class="team-avatar-mini">${team.name_kr[0]}</div>
                        <div>
                            <div class="team-title">${team.name_kr} <span style="font-size:0.75rem; color:var(--text-muted); font-weight:400;">(${team.name})</span></div>
                            <div class="team-desc-small" title="${team.description}">${team.description}</div>
                        </div>
                    </div>
                </td>
                <td class="elo-cell font-outfit">${team.elo}</td>
                <td class="num-cell font-outfit" style="color: var(--color-primary);">${team.attack.toFixed(2)}</td>
                <td class="num-cell font-outfit" style="color: #ef4444;">${team.defense.toFixed(2)}</td>
                <td>
                    <div class="form-dots">
                        ${team.form.map(f => `<span class="form-dot ${f.toLowerCase()}" title="${f}"></span>`).join("")}
                    </div>
                </td>
            `;
            standingsBody.appendChild(tr);
        });
    }

    /* ----------------------------------------------------
       3. 실시간 경기 시뮬레이터 (몬테카를로)
       ---------------------------------------------------- */
    btnSimulate.addEventListener("click", () => {
        const homeName = document.getElementById("sim-home-name").value.trim() || "FC 홈팀";
        const awayName = document.getElementById("sim-away-name").value.trim() || "FC 원정팀";
        
        const payload = {
            home: {
                attack: parseInt(homeAttSlider.value),
                defense: parseInt(homeDefSlider.value),
                form: parseInt(homeFormSlider.value),
                home_advantage: homeAdvCheck.checked
            },
            away: {
                attack: parseInt(awayAttSlider.value),
                defense: parseInt(awayDefSlider.value),
                form: parseInt(awayFormSlider.value)
            }
        };

        // 시뮬레이터 UI 활성화 및 로딩 연출
        simResultBox.classList.remove("hidden");
        simResultBox.classList.add("calculating");
        
        // 스크롤 포커스 이동
        simResultBox.scrollIntoView({ behavior: 'smooth', block: 'nearest' });

        // 몬테카를로 연산의 웅장함을 위해 800ms 지연 연출
        setTimeout(() => {
            fetch("/api/simulate", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(payload)
            })
            .then(res => res.json())
            .then(result => {
                simResultBox.classList.remove("calculating");
                
                // 1. 게이지 채우기
                const hBar = document.getElementById("sim-bar-home");
                const dBar = document.getElementById("sim-bar-draw");
                const aBar = document.getElementById("sim-bar-away");
                
                hBar.style.width = `${result.home_win_p}%`;
                dBar.style.width = `${result.draw_p}%`;
                aBar.style.width = `${result.away_win_p}%`;
                
                hBar.innerHTML = `홈 승(${homeName}) <span id="sim-val-home">${result.home_win_p}%</span>`;
                dBar.innerHTML = `무승부 <span id="sim-val-draw">${result.draw_p}%</span>`;
                aBar.innerHTML = `원정 승(${awayName}) <span id="sim-val-away">${result.away_win_p}%</span>`;
                
                // 2. xG 스코어 대조
                document.getElementById("sim-xg-home").textContent = result.home_xg;
                document.getElementById("sim-xg-away").textContent = result.away_xg;
                
                // 3. 탑 3 스코어 렌더링
                const scoresList = document.getElementById("sim-scores-list");
                scoresList.innerHTML = "";
                
                result.top_scores.forEach((item, idx) => {
                    const li = document.createElement("li");
                    li.className = "top-score-item";
                    li.innerHTML = `
                        <div>
                            <span style="font-size:0.75rem; color:var(--text-muted); font-weight:700; margin-right:8px;">${idx + 1}위</span>
                            <span class="score-badge">${item.score}</span>
                        </div>
                        <span class="score-prob-val ${idx > 0 ? 'cyan-color' : ''}">${item.probability}% 확률</span>
                    `;
                    scoresList.appendChild(li);
                });
            })
            .catch(err => {
                simResultBox.classList.remove("calculating");
                console.error("시뮬레이션 연산 실패:", err);
                alert("시뮬레이션 가동 중 서버 오류가 발생했습니다.");
            });
        }, 800);
    });

    /* ----------------------------------------------------
       4. 예측 상세 리포트 모달 제어
       ---------------------------------------------------- */
    function openPredictionModal(leagueKey, homeId, awayId) {
        // 모달 열기 및 초기 대기 UI 처리
        predictModal.classList.remove("hidden");
        document.body.style.overflow = "hidden"; // 배경 스크롤 방지
        
        // 모달 데이터 필드 초기 클리어
        document.getElementById("modal-home-name").textContent = "분석 중...";
        document.getElementById("modal-away-name").textContent = "분석 중...";
        document.getElementById("modal-home-player").textContent = "";
        document.getElementById("modal-away-player").textContent = "";
        document.getElementById("modal-insight-text").innerHTML = "<div class='spinner' style='width:24px; height:24px; margin:20px auto;'></div>";
        
        // API 요청
        fetch(`/api/predict?league=${leagueKey}&home=${homeId}&away=${awayId}`)
            .then(res => res.json())
            .then(data => {
                // 팀 기본 정보 바인딩
                document.getElementById("modal-home-name").textContent = data.home_team;
                document.getElementById("modal-away-name").textContent = data.away_team;
                
                document.getElementById("modal-home-player").innerHTML = `에이스: <strong>${data.home_details.key_player}</strong>`;
                document.getElementById("modal-away-player").innerHTML = `에이스: <strong>${data.away_details.key_player}</strong>`;
                
                // 기대 승무패 게이지 바 렌더링
                const gHome = document.getElementById("modal-gauge-home");
                const gDraw = document.getElementById("modal-gauge-draw");
                const gAway = document.getElementById("modal-gauge-away");
                
                gHome.style.width = `${data.home_win_p}%`;
                gDraw.style.width = `${data.draw_p}%`;
                gAway.style.width = `${data.away_win_p}%`;
                
                document.getElementById("modal-lbl-home").textContent = `${data.home_win_p}%`;
                document.getElementById("modal-lbl-draw").textContent = `${data.draw_p}%`;
                document.getElementById("modal-lbl-away").textContent = `${data.away_win_p}%`;
                
                // Over / Under 2.5골 진행바
                document.getElementById("modal-bar-over").style.width = `${data.over_2_5_p}%`;
                document.getElementById("modal-bar-under").style.width = `${data.under_2_5_p}%`;
                document.getElementById("modal-val-over").textContent = `${data.over_2_5_p}%`;
                document.getElementById("modal-val-under").textContent = `${data.under_2_5_p}%`;
                
                // BTTS (양팀 득점 확률) 서클 SVG 렌더링
                const bttsVal = data.btts_p;
                document.getElementById("modal-val-btts").textContent = `${bttsVal}%`;
                // SVG stroke-dasharray 값 갱신 (반지름 기반 둘레가 정확히 100이므로 100 기준 맵핑 가능)
                document.getElementById("modal-btts-circle-fill").setAttribute("stroke-dasharray", `${bttsVal}, 100`);
                
                // 탑 3 스코어 보드
                const scoresList = document.getElementById("modal-scores-list");
                scoresList.innerHTML = "";
                data.top_scores.forEach((item, idx) => {
                    const li = document.createElement("li");
                    li.className = "top-score-item";
                    li.innerHTML = `
                        <div>
                            <span style="font-size:0.75rem; color:var(--text-muted); font-weight:700; margin-right:8px;">${idx+1}위</span>
                            <span class="score-badge">${item.score}</span>
                        </div>
                        <span class="score-prob-val ${idx > 0 ? 'cyan-color' : ''}">${item.probability}% 확률</span>
                    `;
                    scoresList.appendChild(li);
                });
                
                // AI 통계 코멘터리 텍스트 삽입
                document.getElementById("modal-insight-text").innerHTML = data.insight;
            })
            .catch(err => {
                console.error("정밀 분석 로드 실패:", err);
                document.getElementById("modal-insight-text").innerHTML = "<p class='neutral-text'>⚠️ 통계 연산 로딩에 실패했습니다.</p>";
            });
    }

    // 모달 닫기
    const closeModal = () => {
        predictModal.classList.add("hidden");
        document.body.style.overflow = ""; // 스크롤 원복
    };
    modalCloseBtn.addEventListener("click", closeModal);
    modalCloseFooterBtn.addEventListener("click", closeModal);
    
    // 모달 바깥 어두운 배경 영역 클릭 시 닫기 구현
    predictModal.addEventListener("click", (e) => {
        if (e.target === predictModal) {
            closeModal();
        }
    });
});
