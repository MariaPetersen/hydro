import RPi.GPIO as GPIO
import time
import state
from .config import PUMP_PIN
import logging
from logging_config import setup_logging

setup_logging()

logger = logging.getLogger(__name__)

PUMP_PIN = 17
loop_running = False
pump_status = "OFF"


def pump_loop():
    logger.info(f"Starting new loop: time: {state.on_time}, interval: {state.interval}")
    state.loop_running = True
    state.pump_status = "ON"

    try:
        while state.loop_running:
            state.count_down_stop = state.on_time
            logger.info("Pump ON in loop")
            GPIO.output(PUMP_PIN, GPIO.LOW)
            while state.count_down_stop > 0:
                time.sleep(1)
                if not state.loop_running:
                    break
                state.count_down_stop -= 1

            state.count_down_start = state.interval
            logger.info("Pump OFF in loop")
            GPIO.output(PUMP_PIN, GPIO.HIGH)
            while state.count_down_start > 0:
                time.sleep(1)
                if not state.loop_running:
                    break
                state.count_down_start -= 1

    finally:
        state.pump_status = "OFF"
        GPIO.output(PUMP_PIN, GPIO.HIGH)