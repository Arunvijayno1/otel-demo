import requests
import threading

URL = "http://localhost:3000/orders"

def hit_api():
    for _ in range(50):
        try:
            requests.get(URL)
        except:
            pass

threads = []

for _ in range(20):  # 20 concurrent users
    t = threading.Thread(target=hit_api)
    t.start()
    threads.append(t)

for t in threads:
    t.join()

print("🔥 Load test completed")