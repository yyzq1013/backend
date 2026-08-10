from flask import Flask, jsonify, request
import socket

app = Flask(__name__)


def get_client_ip():
    xff = request.headers.get('X-Forwarded-For')
    if xff:
        return xff.split(',')[0].strip()
    xrip = request.headers.get('X-Real-IP')
    if xrip:
        return xrip
    return request.remote_addr


@app.route("/api/hello")
def hello():
    client_ip = get_client_ip()
    return jsonify({
        "message": "Hello from Flask backend",
        "status": "ok",
        "Real-IP": client_ip,
        "hostname": socket.gethostname(),
        "X-Forwarded-For": request.headers.get("X-Forwarded-For"),
        "remote_addr": request.remote_addr
    })


@app.route("/api/info")
def info():
    client_ip = get_client_ip()
    return jsonify({
        "service": "flask-demo",
        "version": "1.0",
        "Real-IP": client_ip
    })


if __name__ == "__main__":
    # 非常关键：必须监听 0.0.0.0，否则外部访问不到
    app.run(host="0.0.0.0", port=8000)
