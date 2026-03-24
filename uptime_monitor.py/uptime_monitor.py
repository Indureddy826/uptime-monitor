import requests
import time
import csv
from datetime import datetime

# Websites to monitor
websites = [
    "https://www.google.com",
    "https://www.github.com",
    "https://www.stackoverflow.com"
]

# CSV file
FILE_NAME = "uptime_logs.csv"

# Create CSV file
with open(FILE_NAME, "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Time", "Website", "Status", "Response Time"])

# Uptime tracking
uptime_count = {site: 0 for site in websites}
total_checks = {site: 0 for site in websites}

def check_website(url):
    try:
        start = time.time()
        response = requests.get(url, timeout=5)
        response_time = round(time.time() - start, 2)

        if response.status_code == 200:
            status = "UP"
        else:
            status = "DOWN"

    except:
        status = "DOWN"
        response_time = "N/A"

    return status, response_time

# Main loop
while True:
    for site in websites:
        status, response_time = check_website(site)
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        total_checks[site] += 1
        if status == "UP":
            uptime_count[site] += 1

        uptime_percentage = (uptime_count[site] / total_checks[site]) * 100

        print(f"{now} | {site} | {status} | {response_time}s | Uptime: {uptime_percentage:.2f}%")

        # Save to CSV
        with open(FILE_NAME, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([now, site, status, response_time])

        # Alert (console only)
        if status == "DOWN":
            print(f"⚠️ ALERT: {site} is DOWN!")

    time.sleep(10)