import requests
import time

try:
    from config import PICO_IP #Be careful about dynamic IP
except ImportError:
    PICO_IP = None
    print("Warning: PICO_IP not set. Ensure config.py exists.")


def send_command(command):
    url = f"{PICO_IP}/{command}"
    try:
        response = requests.get(url, timeout=3)
        return response.text
    except requests.exceptions.RequestException as e:
        print("Failed to connect to Pico:", e)
        return False

def ping_pico(_=None):
    try:
        response = requests.get(PICO_IP, timeout=3)  # Send a basic GET request
        if response.status_code == 200:
            return True
        return False
    except requests.exceptions.RequestException:
        return False
    
def led_on(_=None):
    return send_command("led/on")

def led_off(_=None):
    return send_command("led/off")

def detect_cup(_=None):
    return send_command("detect_cup")

def advance_turntable(_=None):
    return send_command("advance_turntable")

if __name__ == "__main__":
    while True:
        led_on()
        time.sleep(1)
        led_off()
        time.sleep(1)
        print("Result of ping: " + str(ping_pico()))