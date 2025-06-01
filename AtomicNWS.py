import time
from datetime import datetime, timezone, timedelta
from collections import deque
import pytz
from noaa_sdk import NOAA
from playsound3 import playsound
from colorama import Fore, Style, Back, init
import gc

init(convert=True)

print()

DESIRED_ALERTS = []
EMERGENCY_ALERTS = []
TIMEZONE = ""
TIME_SCOPE = 30
STATE = ""
LOG = ""
PLAYSOUND = ""
PRINTSETTINGS = ""


MAX_ALERTS = 300
SEEN_ALERT_IDS = deque(maxlen=MAX_ALERTS)  # Store (alert_id, timestamp) for cleanup


def main():
    print("\n\t======Atomic Inc. National Weather Service / NOAA Receiver (C)2025 - All Rights Reserved======\n\n")
    pullSettings()

    if PRINTSETTINGS == "true":
        time.sleep(1)
        print("CURRENT SETTINGS:")
        print(f"Desired Alerts: {DESIRED_ALERTS}\n"
              f"Emergency Alerts: {EMERGENCY_ALERTS}\n"
              f"Timezone: {TIMEZONE}\n"
              f"Time Scope: {TIME_SCOPE}\n"
              f"State: {STATE}\n"
              f"Log: {LOG}\n"
              f"Play Sound: {PLAYSOUND}\n"
              f"Print Settings: {PRINTSETTINGS}")
        print(f"----------------------------------------------\nAlerts in the last {TIME_SCOPE} minutes:")

    else:
        print(f"----------------------------------------------\nAlerts in the last {TIME_SCOPE} minutes:")

    noaa = NOAA()

    while True:
        now = datetime.now(timezone.utc)
        recent = now - timedelta(minutes=TIME_SCOPE)

        ###Keep double length of time_scope
        prune_seen_alerts(now - timedelta(hours=(TIME_SCOPE * 2)))

        getAlert(noaa, now, recent)

        ###Pause between checks
        time.sleep(10)

        ###Explicit garbage collection after a set number of alerts
        if len(SEEN_ALERT_IDS) % MAX_ALERTS == 0:
            gc.collect()


def prune_seen_alerts(cutoff_time):
    while SEEN_ALERT_IDS and SEEN_ALERT_IDS[0][1] < cutoff_time:
        SEEN_ALERT_IDS.popleft()


def getAlert(noaa, now, recent):
    alerts = noaa.alerts()

    if STATE != ['']:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Searching for specified alerts in {STATE}...")
    else:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Searching for specified alerts nationwide...")

    seen_ids_set = set(alert_id for alert_id, _ in SEEN_ALERT_IDS)

    for feature in alerts.get("features", []):
        alert_id = feature.get("id")
        if alert_id in seen_ids_set:
            continue

        properties = feature.get("properties", {})
        timeSent = properties.get("sent")
        timetime = datetime.fromisoformat(timeSent.replace("Z", "+00:00"))

        if timetime > recent:
            location = properties.get("areaDesc")

            if STATE and not any(str(s) in location for s in STATE):
                continue

            if properties.get("event") in DESIRED_ALERTS:
                SEEN_ALERT_IDS.append((alert_id, now))

                sent_time_str = properties.get("sent")
                sent_time = datetime.fromisoformat(sent_time_str.replace("Z", "+00:00"))
                defined_time_zone = sent_time.astimezone(pytz.timezone(TIMEZONE)).strftime('%Y-%m-%d %H:%M:%S')
                event_title = properties.get("event")

                if properties.get("event") in EMERGENCY_ALERTS:
                    description = properties.get("description")
                    printAlert_Desc(defined_time_zone, event_title, location, description)
                else:
                    printAlert(defined_time_zone, event_title, location)


def printAlert(defined_time_zone, event_title, location):
    print()
    print(Style.RESET_ALL + f"[{defined_time_zone}]" + Fore.BLUE + f" {event_title}" + Style.RESET_ALL + f" at ({location})")
    print()
    if LOG == "true":
        writeToFile(defined_time_zone, event_title, location, "", False)


def printAlert_Desc(defined_time_zone, event_title, location, description):
    cancellation = "has been cancelled and is no longer in effect."

    if cancellation not in description:
        print("\n----------------------------------------------")
        print(Back.RED + Fore.WHITE + Style.BRIGHT + f"EMERGENCY ALERT:\n[{defined_time_zone}] {event_title} at ({location}).\n" +
              Style.RESET_ALL + f"Description: {description}\n")
        print("----------------------------------------------\n")

        if LOG == "true":
            writeToFile(defined_time_zone, event_title, location, description, True)

        if PLAYSOUND == "true":
            playsound("Same.wav")


def pullSettings():
    global DESIRED_ALERTS, EMERGENCY_ALERTS, TIMEZONE, TIME_SCOPE, STATE, LOG, PLAYSOUND, PRINTSETTINGS

    with open("settings.txt", 'r') as file:
        for line in file:
            if line.startswith("desired_alerts"):
                values = line.split("=", 1)[1].strip()
                DESIRED_ALERTS = [item.strip().strip('"') for item in values.split(",")]
            elif line.startswith("emergency_alerts"):
                values = line.split("=", 1)[1].strip()
                EMERGENCY_ALERTS = [item.strip().strip('"') for item in values.split(",")]
            elif line.startswith("timezone"):
                TIMEZONE = line.split("=", 1)[1].strip().strip('"')
            elif line.startswith("time_within"):
                TIME_SCOPE = int(line.split("=", 1)[1].strip())
            elif line.startswith("state"):
                values = line.split("=", 1)[1].strip()
                STATE = [item.strip().strip('"') for item in values.split(",")]
            elif line.startswith("write_to_file"):
                LOG = line.split("=", 1)[1].strip().strip('"')
            elif line.startswith("play_sound"):
                PLAYSOUND = line.split("=", 1)[1].strip().strip('"')
            elif line.startswith("printsettings"):
                PRINTSETTINGS = line.split("=", 1)[1].strip().strip('"')


def writeToFile(defined_time_zone, event_title, location, description, emergency):
    with open("log.txt", "a") as file:
        if not emergency:
            file.write(f"[{defined_time_zone}] {event_title} at ({location})\n")
        else:
            file.write(
                f"\n----------------------------------------------\nEMERGENCY ALERT:\n[{defined_time_zone}] {event_title} at ({location}).\n Description: {description}\n----------------------------------------------\n")


main()
