import requests
import time

# Replace with the IP address of the Pico W (check in the console output of the Pico W)
#This could change with MIT's dymaic IP allocation. Be careful
PICO_IP = "http://10.29.240.252"

def send_command(command):
    url = f"{PICO_IP}/{command}"
    try:
        return requests.get(url).text
    except requests.exceptions.RequestException as e:
        print("Failed to connect to Pico:", e)

def control_led(command):
    url = f"{PICO_IP}/led/{command}"
    try:
        response = requests.get(url)
        print("Response from Pico:", response.text)
    except requests.exceptions.RequestException as e:
        print("Failed to connect to Pico:", e)

def led_on(_):
    control_led("on")

def led_off(_):
    control_led("off")

def ping_pico(_=None):
    try:
        response = requests.get(PICO_IP, timeout=2)  # Send a basic GET request
        if response.status_code == 200:
            return True
    except requests.exceptions.RequestException:
        return False