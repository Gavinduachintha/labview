from collectors import cpu, disk, ram
from flask import Flask, jsonify, render_template

app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


@app.route("/api", methods=["GET"])
def service_info():
    return jsonify({
        "service": "LabView System Monitoring API",
        "status": "running",
        "endpoint": "/status"
    })


@app.route("/status", methods=["GET"])
def get_status():

    status = {
        "cpu": cpu.get_cpu_usage(),
        "ram": ram.get_ram_usage(),
        "disk": disk.get_disk_usage()
    }

    return jsonify(status)


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )