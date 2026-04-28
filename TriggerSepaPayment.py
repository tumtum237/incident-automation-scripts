import requests
import time

TOKEN = "TOKEN"
URL = "Url/invoiceid/settle-sepa"

with open("ids.csv", "r") as f, open("result.log", "a") as log:
    for line in f:
        invoiceid = line.strip()

        if not invoiceid:
            continue

        log.write(f"Processing invoice {invoiceid}\n")
        print(f"Processing invoice {invoiceid}")

        response = requests.post(
            URL.format(invoiceid),
            headers={
                "Authorization": f"Bearer {TOKEN}",
                "Content-Type": "application/json"
            },
            json={}
        )

        log.write(f"Status: {response.status_code}\n")
        log.write(f"Response: {response.text}\n")
        log.write("----------------------\n")

        time.sleep(0.1)