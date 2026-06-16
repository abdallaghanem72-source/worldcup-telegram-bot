import requests
import json
from datetime import datetime, timedelta

BOT_TOKEN = "PUT_YOUR_BOT_TOKEN"
CHAT_ID = "1407218144"

# مصدر مجاني للمباريات (TheSportsDB free endpoint)
API_URL = "https://www.thesportsdb.com/api/v1/json/3/eventsnextleague.php?id=4520"

sent_matches_file = "sent.json"

def load_sent():
    try:
        with open(sent_matches_file, "r") as f:
            return json.load(f)
    except:
        return []

def save_sent(data):
    with open(sent_matches_file, "w") as f:
        json.dump(data, f)

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})

def get_matches():
    res = requests.get(API_URL)
    data = res.json()
    return data.get("events", [])

def parse_time(t):
    try:
        return datetime.strptime(t, "%Y-%m-%d %H:%M:%S")
    except:
        return None

def main():
    matches = get_matches()
    sent = load_sent()

    now = datetime.utcnow()

    for m in matches:
        match_id = m["idEvent"]

        if match_id in sent:
            continue

        home = m["strHomeTeam"]
        away = m["strAwayTeam"]
        time = parse_time(m["dateEvent"] + " " + m["strTime"])

        if not time:
            continue

        # قبل الماتش بـ 10 دقائق
        if now >= time - timedelta(minutes=10) and now < time:
            msg = f"""🔔 مباراة بعد 10 دقائق

{home} 🆚 {away}
🏆 كأس العالم 2026
🕒 {time}

استعد ⚽"""
            send_telegram(msg)

        # بعد بداية الوقت (تقريب للنتيجة)
        if now >= time:
            score = f"{home} vs {away}"

            msg = f"""✅ المباراة بدأت/انتهت

{score}

تابع النتيجة النهائية في التطبيق ⚽"""
            send_telegram(msg)

            sent.append(match_id)
            save_sent(sent)

if name == "main":
    main()
