from flask import Flask, jsonify
from valve.source.a2s import ServerQuerier

app = Flask(__name__)

SERVER_IP = "62.122.215.81"
SERVER_PORT = 27015

@app.route("/")
def home():
    return jsonify({"status": "API is running"})

@app.route("/status")
def status():
    try:
        with ServerQuerier((SERVER_IP, SERVER_PORT)) as server:
            info = server.info()
            players = server.players()
            return jsonify({
                "server_name": info['server_name'],
                "map": info['map'],
                "players_online": info['player_count'],
                "max_players": info['max_players'],
                "players": [
                    {"name": p['name'], "score": p['score'], "time": round(p['duration'], 1)}
                    for p in players['players']
                ]
            })
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)