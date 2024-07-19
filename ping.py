import requests

def get_ping():
    url = "https://api.uptimerobot.com/v2/getMonitors"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer YOUR_UPTIMEROBOT_API_KEY"  # APIキーをここに入力
    }
    response = requests.get(url, headers=headers)
    data = response.json()
    for monitor in data['monitors']:
        if monitor['friendly_name'] == 'Your Monitor Name':
            return monitor['status']
    return "Not Found"

if __name__ == "__main__":
    ping = get_ping()
    print(f"Ping Status: {ping}")
