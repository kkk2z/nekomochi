from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ping')
def ping():
    try:
        response = requests.get("https://api.uptimerobot.com/v2/getMonitors", headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer YOUR_UPTIMEROBOT_API_KEY"
        })
        data = response.json()
        for monitor in data['monitors']:
            if monitor['friendly_name'] == 'Your Monitor Name':
                return jsonify({'ping': monitor['status']})
        return jsonify({'ping': 'Not Found'})
    except Exception as e:
        return jsonify({'ping': str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
