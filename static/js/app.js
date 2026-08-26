
document.addEventListener("DOMContentLoaded", () => {
    // cached league data
    let cachedLeagues = null;

    // DOM references
    const fixturesGrid = document.getElementById("fixtures-grid");
    const standingsBody = document.getElementById("standings-body");
    const leagueTabBtns = document.querySelectorAll(".league-tab-btn");
    
    // simulator controls
    const btnSimulate = document.getElementById("btn-run-simulation");
    const simResultBox = document.getElementById("sim-result-box");
    const homeAttSlider = document.getElementById("sim-home-attack");
    const homeDefSlider = document.getElementById("sim-home-defense");
    const homeFormSlider = document.getElementById("sim-home-form");
    const homeAdvCheck = document.getElementById("sim-home-adv");
    
    const awayAttSlider = document.getElementById("sim-away-attack");
    const awayDefSlider = document.getElementById("sim-away-defense");
    const awayFormSlider = document.getElementById("sim-away-form");
    
    // slider value labels
    const homeAttVal = document.getElementById("home-att-val");
    const homeDefVal = document.getElementById("home-def-val");
    const homeFormVal = document.getElementById("home-form-val");
    const awayAttVal = document.getElementById("away-att-val");
    const awayDefVal = document.getElementById("away-def-val");
    const awayFormVal = document.getElementById("away-form-val");

    // modal
    const predictModal = document.getElementById("predict-modal");
    const modalCloseBtn = document.getElementById("modal-close-btn");
    const modalCloseFooterBtn = document.getElementById("modal-close-footer-btn");

    /* ----------------------------------------------------
       1. Initialisation and slider bindings
       ---------------------------------------------------- */
    // keep the numeric label in sync with the slider
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

    // initial data load
    loadFixtures();
    loadLeaguesAndStandings();

    /* ----------------------------------------------------
       2. API calls and rendering
       ---------------------------------------------------- */
    // fetch live and upcoming fixtures
    function loadFixtures() {
        fetch("/api/fixtures")
            .then(res => res.json())
            .then(fixtures => {
                fixturesGrid.innerHTML = "";
                if (fixtures.length === 0) {
                    fixturesGrid.innerHTML = "<p class='neutral-text'>No matches are live or scheduled right now.</p>";
                    return;
                }
                
                fixtures.forEach(fix => {
                    const card = document.createElement("div");
                    card.className = `fixture-card ${fix.featured ? 'featured' : ''} ${fix.state === 'in' ? 'live-border' : ''}`;
                    
                    // club badge from ESPN, falling back to an initial
                    const homeLogoHtml = fix.home.logo 
                        ? `<img src="${fix.home.logo}" class="team-logo-img" alt="${fix.home.name}">` 
                        : `<div class="team-avatar">${fix.home.name[0]}</div>`;
                        
                    const awayLogoHtml = fix.away.logo 
                        ? `<img src="${fix.away.logo}" class="team-logo-img" alt="${fix.away.name}">` 
                        : `<div class="team-avatar">${fix.away.name[0]}</div>`;
                    
                    // score display for live and finished matches
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

                    // status tag styling
                    const tagClass = fix.state === 'in' ? 'tag-live-pulsing' : (fix.state === 'post' ? 'tag-finished' : '');

                    card.innerHTML = `
                        <div class="card-top">
                            <span class="league-badge" style="background: linear-gradient(135deg, rgba(255,255,255,0.1), rgba(255,255,255,0.05)); border: 1px solid rgba(255,255,255,0.15);">${fix.league_name}</span>
                            <span class="match-time-tag ${tagClass}">${fix.status_text}</span>
                        </div>
                        <div class="match-teams-row">
                            <div class="team-block">
                                <div class="logo-wrapper">${homeLogoHtml}</div>
                                <div class="team-name">${fix.home.name}</div>
                                <div class="team-stat-sub">Elo: ${fix.home.elo}</div>
                            </div>
                            ${vsHtml}
                            <div class="team-block">
                                <div class="logo-wrapper">${awayLogoHtml}</div>
                                <div class="team-name">${fix.away.name}</div>
                                <div class="team-stat-sub">Elo: ${fix.away.elo}</div>
                            </div>
                        </div>
                        <div class="card-action">
                            <div class="form-dots">
                                ${fix.home.form.slice(-3).map(f => `<span class="form-dot ${f.toLowerCase()}" title="Home form: ${f}"></span>`).join("")}
                                <span style="font-size:0.7rem; color:var(--text-muted); padding:0 3px;">vs</span>
                                ${fix.away.form.slice(-3).map(f => `<span class="form-dot ${f.toLowerCase()}" title="Away form: ${f}"></span>`).join("")}
                            </div>
                            <a class="btn-predict-link">Full analysis &rarr;</a>
                        </div>
                    `;
                    
                    // open the detail modal on click
                    card.addEventListener("click", () => {
                        openPredictionModal(fix.league_key, fix.home.id, fix.away.id);
                    });
                    
                    fixturesGrid.appendChild(card);
                });
            })
            .catch(err => {
                console.error("Failed to load fixtures:", err);
                fixturesGrid.innerHTML = "<p class='neutral-text'>⚠️ Could not load fixtures.</p>";
            });
    }

    // load league data and bind tab clicks
    function loadLeaguesAndStandings() {
        fetch("/api/leagues")
            .then(res => res.json())
            .then(data => {
                cachedLeagues = data;
                // render the default tab
                renderStandings("epl");
            })
            .catch(err => {
                console.error("Failed to load leagues:", err);
                standingsBody.innerHTML = "<tr><td colspan='5' class='neutral-text'>⚠️ Could not load team ratings.</td></tr>";
            });

        // league tab handlers
        leagueTabBtns.forEach(btn => {
            btn.addEventListener("click", () => {
                leagueTabBtns.forEach(b => b.classList.remove("active"));
                btn.classList.add("active");
                const leagueKey = btn.getAttribute("data-league");
                renderStandings(leagueKey);
            });
        });
    }

    // render the ratings table
    function renderStandings(leagueKey) {
        if (!cachedLeagues || !cachedLeagues[leagueKey]) return;
        
        const league = cachedLeagues[leagueKey];
        const teams = league.teams;
        standingsBody.innerHTML = "";
        
        // sort clubs by Elo, highest first
        const sortedTeams = Object.keys(teams).map(key => ({
            id: key,
            ...teams[key]
        })).sort((a, b) => b.elo - a.elo);
        
        sortedTeams.forEach(team => {
            const tr = document.createElement("tr");
            tr.innerHTML = `
                <td>
                    <div class="team-info-cell">
                        <div class="team-avatar-mini">${team.name[0]}</div>
                        <div>
                            <div class="team-title">${team.name}</div>
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
       3. Monte Carlo simulator
       ---------------------------------------------------- */
    btnSimulate.addEventListener("click", () => {
        const homeName = document.getElementById("sim-home-name").value.trim() || "Home team";
        const awayName = document.getElementById("sim-away-name").value.trim() || "Away team";
        
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

        // show the result panel in a loading state
        simResultBox.classList.remove("hidden");
        simResultBox.classList.add("calculating");
        
        // bring the results into view
        simResultBox.scrollIntoView({ behavior: 'smooth', block: 'nearest' });

        // brief delay so the loading state is visible
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
                
                // outcome bars
                const hBar = document.getElementById("sim-bar-home");
                const dBar = document.getElementById("sim-bar-draw");
                const aBar = document.getElementById("sim-bar-away");
                
                hBar.style.width = `${result.home_win_p}%`;
                dBar.style.width = `${result.draw_p}%`;
                aBar.style.width = `${result.away_win_p}%`;
                
                hBar.innerHTML = `Home &mdash; ${homeName} <span id="sim-val-home">${result.home_win_p}%</span>`;
                dBar.innerHTML = `Draw <span id="sim-val-draw">${result.draw_p}%</span>`;
                aBar.innerHTML = `Away &mdash; ${awayName} <span id="sim-val-away">${result.away_win_p}%</span>`;
                
                // expected goals
                document.getElementById("sim-xg-home").textContent = result.home_xg;
                document.getElementById("sim-xg-away").textContent = result.away_xg;
                
                // most likely scorelines
                const scoresList = document.getElementById("sim-scores-list");
                scoresList.innerHTML = "";
                
                result.top_scores.forEach((item, idx) => {
                    const li = document.createElement("li");
                    li.className = "top-score-item";
                    li.innerHTML = `
                        <div>
                            <span style="font-size:0.75rem; color:var(--text-muted); font-weight:700; margin-right:8px;">#${idx + 1}</span>
                            <span class="score-badge">${item.score}</span>
                        </div>
                        <span class="score-prob-val ${idx > 0 ? 'cyan-color' : ''}">${item.probability}%</span>
                    `;
                    scoresList.appendChild(li);
                });
            })
            .catch(err => {
                simResultBox.classList.remove("calculating");
                console.error("Simulation request failed:", err);
                alert("The simulation could not be completed. Please try again.");
            });
        }, 800);
    });

    /* ----------------------------------------------------
       4. Match detail modal
       ---------------------------------------------------- */
    function openPredictionModal(leagueKey, homeId, awayId) {
        // open the modal in a loading state
        predictModal.classList.remove("hidden");
        document.body.style.overflow = "hidden"; // lock background scroll
        
        // clear previous values
        document.getElementById("modal-home-name").textContent = "Analysing...";
        document.getElementById("modal-away-name").textContent = "Analysing...";
        document.getElementById("modal-home-player").textContent = "";
        document.getElementById("modal-away-player").textContent = "";
        document.getElementById("modal-insight-text").innerHTML = "<div class='spinner' style='width:24px; height:24px; margin:20px auto;'></div>";
        
        // request the prediction
        fetch(`/api/predict?league=${leagueKey}&home=${homeId}&away=${awayId}`)
            .then(res => res.json())
            .then(data => {
                // team details
                document.getElementById("modal-home-name").textContent = data.home_team;
                document.getElementById("modal-away-name").textContent = data.away_team;
                
                document.getElementById("modal-home-player").innerHTML = `Key player: <strong>${data.home_details.key_player}</strong>`;
                document.getElementById("modal-away-player").innerHTML = `Key player: <strong>${data.away_details.key_player}</strong>`;
                
                // outcome gauge
                const gHome = document.getElementById("modal-gauge-home");
                const gDraw = document.getElementById("modal-gauge-draw");
                const gAway = document.getElementById("modal-gauge-away");
                
                gHome.style.width = `${data.home_win_p}%`;
                gDraw.style.width = `${data.draw_p}%`;
                gAway.style.width = `${data.away_win_p}%`;
                
                document.getElementById("modal-lbl-home").textContent = `${data.home_win_p}%`;
                document.getElementById("modal-lbl-draw").textContent = `${data.draw_p}%`;
                document.getElementById("modal-lbl-away").textContent = `${data.away_win_p}%`;
                
                // over/under 2.5 goals
                document.getElementById("modal-bar-over").style.width = `${data.over_2_5_p}%`;
                document.getElementById("modal-bar-under").style.width = `${data.under_2_5_p}%`;
                document.getElementById("modal-val-over").textContent = `${data.over_2_5_p}%`;
                document.getElementById("modal-val-under").textContent = `${data.under_2_5_p}%`;
                
                // both teams to score
                const bttsVal = data.btts_p;
                document.getElementById("modal-val-btts").textContent = `${bttsVal}%`;
                // the circle circumference is 100, so the percentage maps directly
                document.getElementById("modal-btts-circle-fill").setAttribute("stroke-dasharray", `${bttsVal}, 100`);
                
                // most likely scorelines
                const scoresList = document.getElementById("modal-scores-list");
                scoresList.innerHTML = "";
                data.top_scores.forEach((item, idx) => {
                    const li = document.createElement("li");
                    li.className = "top-score-item";
                    li.innerHTML = `
                        <div>
                            <span style="font-size:0.75rem; color:var(--text-muted); font-weight:700; margin-right:8px;">#${idx+1}</span>
                            <span class="score-badge">${item.score}</span>
                        </div>
                        <span class="score-prob-val ${idx > 0 ? 'cyan-color' : ''}">${item.probability}%</span>
                    `;
                    scoresList.appendChild(li);
                });
                
                // model commentary
                document.getElementById("modal-insight-text").innerHTML = data.insight;
            })
            .catch(err => {
                console.error("Prediction request failed:", err);
                document.getElementById("modal-insight-text").innerHTML = "<p class='neutral-text'>⚠️ Could not load the analysis.</p>";
            });
    }

    // close the modal
    const closeModal = () => {
        predictModal.classList.add("hidden");
        document.body.style.overflow = ""; // restore scroll
    };
    modalCloseBtn.addEventListener("click", closeModal);
    modalCloseFooterBtn.addEventListener("click", closeModal);
    
    // close when the backdrop is clicked
    predictModal.addEventListener("click", (e) => {
        if (e.target === predictModal) {
            closeModal();
        }
    });
});
