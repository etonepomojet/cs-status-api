from flask import Flask, jsonify
from valve.source.a2s import ServerQuerier
import socket

app = Flask(__name__)

SERVER_ADDRESS = ("62.122.215.81", 27015)  # замените на свой IP и порт

@app.route("/status")
def status():
    return jsonify({"status": "API is running"})

@app.route("/server-info")
def server_info():
    try:
        with ServerQuerier(SERVER_ADDRESS) as server:
            info = server.info()      # заменено с get_info()
            players = server.players()  # заменено с get_players()

        return jsonify({
            "server_name": info["server_name"],
            "map": info["map"],
            "player_count": info["player_count"],
            "max_players": info["max_players"],
            "players": [p["name"] for p in players["players"]]
        })
    except socket.timeout:
        return jsonify({"error": "Server not responding"}), 504
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
