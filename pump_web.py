import RPi.GPIO as GPIO
import threading
import atexit
import state
from flask import Flask, render_template, redirect, url_for, request

from pump import pump_loop, PUMP_PIN

import logging
from logging_config import setup_logging

setup_logging()

logger = logging.getLogger(__name__)

app = Flask(__name__)
loop_thread = None

GPIO.setmode(GPIO.BCM)
GPIO.setup(PUMP_PIN, GPIO.OUT)
GPIO.output(PUMP_PIN, GPIO.HIGH)

def cleanup():
    logger.info("Cleaning up... Turning off the pump.")
    GPIO.output(PUMP_PIN, GPIO.HIGH)  

atexit.register(cleanup)

@app.route("/")
def index():
    return render_template("index.html", 
                           pump_status=state.pump_status, 
                           loop_running=state.loop_running, 
                           count_down_stop=state.count_down_stop, 
                           count_down_start=state.count_down_start, 
                           on_time=state.on_time,
                           interval=state.interval)

@app.route("/on", methods=["POST"])
def pump_on():
    GPIO.output(PUMP_PIN, GPIO.LOW)
    state.pump_status = "ON"
    logger.info("Pump turned ON") 
    return redirect(url_for("index"))

@app.route("/off", methods=["POST"])
def pump_off():
    GPIO.output(PUMP_PIN, GPIO.HIGH)
    state.pump_status = "OFF"
    logger.info("Pump turned OFF") 
    return redirect(url_for("index"))

@app.route("/start-loop", methods=["POST"])
def start_loop():
    global loop_thread
    if state.loop_running:
        logger.info("Stopping existing loop before starting new one...")
        state.loop_running = False
        if loop_thread and loop_thread.is_alive():
            loop_thread.join()
    if not state.loop_running:
        state.interval = float(request.form["interval"])
        state.on_time = float(request.form["duration"])
        state.loop_running = True
        state.pump_status = "ON" 
        logger.info("Starting loop: interval=%s, duration=%s", state.interval, state.on_time)
        loop_thread = threading.Thread(target=pump_loop, daemon=True)
        loop_thread.start()
    return redirect(url_for("index"))

@app.route("/stop-loop", methods=["POST"])
def stop_loop():
    GPIO.output(PUMP_PIN, GPIO.HIGH)
    state.loop_running = False
    state.pump_status = "OFF"
    logger.info("Loop stopped")
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)