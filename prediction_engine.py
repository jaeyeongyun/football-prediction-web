
import math
import random
from database import LEAGUE_DATA

def poisson_probability(lmbda, k):
    """포아송 분포 확률 계산: P(k; lambda) = (lambda^k * e^-lambda) / k!"""
    if lmbda <= 0:
        return 1.0 if k == 0 else 0.0
    return (math.pow(lmbda, k) * math.exp(-lmbda)) / math.factorial(k)

def calculate_form_multiplier(form_list):
    """최근 5경기 결과를 바탕으로 컨디션 승수 계산 (최대 1.1배, 최소 0.9배)"""
    if not form_list:
        return 1.0
    points = 0
    for r in form_list:
        if r == 'W':
            points += 3
        elif r == 'D':
            points += 1
    # 최대 15점, 최소 0점 -> 0.9 ~ 1.1 범위로 선형 맵핑
    max_possible = 15
    ratio = points / max_possible if max_possible > 0 else 0.5
    return 0.9 + (ratio * 0.2) # 0.9 + [0.0 ~ 0.2]

def get_xg(home_team, away_team, league_key=None, home_advantage=1.1, away_disadvantage=0.9):
    """두 팀의 능력치를 기반으로 기대 득점(xG) 계산"""
    # 1. 기본 공격 및 수비력 가져오기
    h_att = home_team.get("attack", 1.5)
    h_def = home_team.get("defense", 1.1)
    a_att = away_team.get("attack", 1.5)
    a_def = away_team.get("defense", 1.1)
    
    # 2. Elo 격차에 따른 전력 보정
    h_elo = home_team.get("elo", 1500)
    a_elo = away_team.get("elo", 1500)
    elo_diff = h_elo - a_elo
    
    # Elo 차이 400점당 기대 득점 보정 인자 (최대 +-40%)
    elo_adjust = elo_diff / 1000.0
    elo_adjust = max(-0.4, min(0.4, elo_adjust))
    
    # 3. 최근 폼 반영
    h_form = calculate_form_multiplier(home_team.get("form", []))
    a_form = calculate_form_multiplier(away_team.get("form", []))
    
    # 4. 기대 득점(xG) 최종 산출
    # 홈 기대 득점 = 홈 공격력 * 원정 수비력 * 홈 이점 * 홈 폼 보정 * Elo 보정 승수
    home_xg = h_att * a_def * home_advantage * h_form * (1.0 + elo_adjust * 0.5)
    # 원정 기대 득점 = 원정 공격력 * 홈 수비력 * 원정 약세 * 원정 폼 보정 * Elo 역보정 승수
    away_xg = a_att * h_def * away_disadvantage * a_form * (1.0 - elo_adjust * 0.5)
    
    # 최소 기대 득점 방어선 (0.2골)
    home_xg = max(0.2, home_xg)
    away_xg = max(0.2, away_xg)
    
    return round(home_xg, 2), round(away_xg, 2)

def generate_prediction(home_team, away_team, league_key=None, custom=False):
    """포아송 분포 모델을 이용한 종합 매치 예측"""
    home_xg, away_xg = get_xg(home_team, away_team, league_key)
    
    # 0골부터 5골까지의 확률 매트릭스 계산
    max_goals = 6  # 0, 1, 2, 3, 4, 5
    prob_matrix = [[0.0 for _ in range(max_goals)] for _ in range(max_goals)]
    
    home_probs = [poisson_probability(home_xg, k) for k in range(max_goals)]
    away_probs = [poisson_probability(away_xg, k) for k in range(max_goals)]
    
    # 확률 매트릭스 채우기 및 정규화(나머지 고득점 확률 보정용)
    sum_prob = 0.0
    for h in range(max_goals):
        for a in range(max_goals):
            p = home_probs[h] * away_probs[a]
            prob_matrix[h][a] = p
            sum_prob += p
            
    # 매트릭스 내의 확률 합이 1이 되도록 정규화
    if sum_prob > 0:
        for h in range(max_goals):
            for a in range(max_goals):
                prob_matrix[h][a] /= sum_prob
                
    # 승/무/패 확률 누적
    home_win_p = 0.0
    draw_p = 0.0
    away_win_p = 0.0
    
    for h in range(max_goals):
        for a in range(max_goals):
            if h > a:
                home_win_p += prob_matrix[h][a]
            elif h == a:
                draw_p += prob_matrix[h][a]
            else:
                away_win_p += prob_matrix[h][a]
                
    # 가장 확률이 높은 스코어 Top 3 산출
    flat_scores = []
    for h in range(max_goals):
        for a in range(max_goals):
            flat_scores.append({
                "score": f"{h} - {a}",
                "home": h,
                "away": a,
                "probability": round(prob_matrix[h][a] * 100, 2)
            })
            
    flat_scores.sort(key=lambda x: x["probability"], reverse=True)
    top_scores = flat_scores[:3]
    
    # Over / Under 2.5 골 확률
    over_2_5 = 0.0
    under_2_5 = 0.0
    for h in range(max_goals):
        for a in range(max_goals):
            if h + a > 2.5:
                over_2_5 += prob_matrix[h][a]
            else:
                under_2_5 += prob_matrix[h][a]
                
    # 양 팀 득점 (BTTS - Both Teams To Score) 확률
    btts_prob = 0.0
    for h in range(1, max_goals):
        for a in range(1, max_goals):
            btts_prob += prob_matrix[h][a]
            
    # 정밀 백분율로 변환
    h_win_pct = round(home_win_p * 100, 1)
    draw_pct = round(draw_p * 100, 1)
    a_win_pct = round(away_win_p * 100, 1)
    
    # 분석 리포트 생성
    insight = generate_insight(home_team, away_team, home_xg, away_xg, h_win_pct, a_win_pct, draw_pct)
    
    return {
        "home_team": home_team.get("name", home_team.get("name_kr")),
        "away_team": away_team.get("name", away_team.get("name_kr")),
        "home_xg": home_xg,
        "away_xg": away_xg,
        "home_win_p": h_win_pct,
        "draw_p": draw_pct,
        "away_win_p": a_win_pct,
        "top_scores": top_scores,
        "over_2_5_p": round(over_2_5 * 100, 1),
        "under_2_5_p": round(under_2_5 * 100, 1),
        "btts_p": round(btts_prob * 100, 1),
        "insight": insight
    }

def run_monte_carlo(home_stats, away_stats, num_simulations=10000):
    """사용자 커스텀 스탯을 기반으로 10,000회 경기 몬테카를로 시뮬레이션 수행"""
    # 1. 기대 득점 계산
    h_att = float(home_stats.get("attack", 50)) / 25.0  # 0~100 게이지 -> 0~4 공격 계수 변환
    h_def = (100.0 - float(home_stats.get("defense", 50))) / 35.0  # 방어력이 높을수록 실점 계수는 작아짐
    h_form_val = float(home_stats.get("form", 50)) / 50.0  # 0.5 ~ 1.5 보정
    
    a_att = float(away_stats.get("attack", 50)) / 25.0
    a_def = (100.0 - float(away_stats.get("defense", 50))) / 35.0
    a_form_val = float(away_stats.get("form", 50)) / 50.0
    
    h_adv = 1.15 if home_stats.get("home_advantage", True) else 1.0
    a_disadv = 0.85 if home_stats.get("home_advantage", True) else 1.0
    
    home_xg = max(0.1, h_att * a_def * h_adv * h_form_val)
    away_xg = max(0.1, a_att * h_def * a_disadv * a_form_val)
    
    # 2. 시뮬레이션 가동
    h_wins = 0
    draws = 0
    a_wins = 0
    score_counts = {}
    
    for _ in range(num_simulations):
        # 포아송 분포 역함수 샘플링 대신 간단하고 표준적인 Knuth의 Poisson 알고리즘 사용
        h_goals = sample_poisson(home_xg)
        a_goals = sample_poisson(away_xg)
        
        # 6골 이상은 5골로 보정 (스코어보드 표현 한계 조절)
        h_goals = min(5, h_goals)
        a_goals = min(5, a_goals)
        
        if h_goals > a_goals:
            h_wins += 1
        elif h_goals == a_goals:
            draws += 1
        else:
            a_wins += 1
            
        score_key = f"{h_goals} - {a_goals}"
        score_counts[score_key] = score_counts.get(score_key, 0) + 1
        
    # 3. 결과 정리
    h_win_pct = round((h_wins / num_simulations) * 100, 1)
    draw_pct = round((draws / num_simulations) * 100, 1)
    a_win_pct = round((a_wins / num_simulations) * 100, 1)
    
    # 스코어 순위 산출
    sorted_scores = sorted(score_counts.items(), key=lambda x: x[1], reverse=True)
    top_scores = []
    for score_str, count in sorted_scores[:3]:
        parts = score_str.split(" - ")
        top_scores.append({
            "score": score_str,
            "home": int(parts[0]),
            "away": int(parts[1]),
            "probability": round((count / num_simulations) * 100, 2)
        })
        
    return {
        "home_xg": round(home_xg, 2),
        "away_xg": round(away_xg, 2),
        "home_win_p": h_win_pct,
        "draw_p": draw_pct,
        "away_win_p": a_win_pct,
        "top_scores": top_scores,
        "simulations": num_simulations
    }

def sample_poisson(lmbda):
    """Knuth의 포아송 난수 생성 알고리즘"""
    L = math.exp(-lmbda)
    k = 0
    p = 1.0
    while p > L:
        k += 1
        p *= random.random()
    return k - 1

def english_player(name):
    """Ratings store players as "한국어 (English)"; return the English part."""
    if name and "(" in name and name.rstrip().endswith(")"):
        return name[name.rfind("(") + 1:name.rfind(")")].strip()
    return name


def generate_insight(home, away, h_xg, a_xg, h_p, a_p, d_p):
    """Return a short written summary of the model output."""
    h_name = home.get("name", home.get("name_kr"))
    a_name = away.get("name", away.get("name_kr"))

    if h_p > a_p + 15:
        verdict = (f"Home advantage and a clear edge in the underlying ratings make "
                   f"**{h_name}** the model's favourite in this fixture.")
    elif a_p > h_p + 15:
        verdict = (f"Despite travelling, **{a_name}** hold a clear advantage in the "
                   f"underlying ratings and are favoured to control this match.")
    elif abs(h_p - a_p) < 10:
        verdict = (f"The two sides are closely matched. {h_name} have home advantage and "
                   f"{a_name} have the means to respond, so a **draw is a live outcome**.")
    else:
        dominant = h_name if h_p > a_p else a_name
        verdict = (f"**{dominant}** hold a modest edge across the ratings and are "
                   f"slightly more likely to dictate the match.")

    total_xg = round(h_xg + a_xg, 2)
    if total_xg >= 2.8:
        goal_comment = (f"Combined expected goals of **{total_xg}** point to an open game "
                        f"with chances at both ends.")
    elif total_xg <= 1.8:
        goal_comment = (f"Combined expected goals of just **{total_xg}** suggest a tight, "
                        f"low-scoring match shaped by both defences.")
    else:
        goal_comment = (f"Combined expected goals of around **{total_xg}** sit close to the "
                        f"league average for a fixture of this profile.")

    h_player = english_player(home.get("key_player", ""))
    a_player = english_player(away.get("key_player", ""))
    player_comment = (f"The likeliest sources of a breakthrough are **{h_player}** for the "
                      f"home side and **{a_player}** for the visitors.")

    return f"{verdict}<br><br>{goal_comment}<br><br>{player_comment}"
