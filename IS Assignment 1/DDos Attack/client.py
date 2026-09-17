import requests
import time

SERVER = "http://192.168.43.120:5000/"

rates = [5, 10, 20, 40, 60]

for rate in rates:
    print("Testing", rate, "requests/second")

    start = time.time()
    successful = 0
    failed = 0

    for i in range(rate * 10):
        try:
            response = requests.get(SERVER, timeout=3)

            if response.status_code == 200:
                successful += 1
            else:
                failed += 1

        except:
            failed += 1

        time.sleep(1 / rate)

    elapsed = time.time() - start

    print("Successful:", successful)
    print("Failed:", failed)
    print("Time:", round(elapsed, 2), "seconds")
    print("----------------------")

    time.sleep(5)