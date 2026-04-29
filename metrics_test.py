import requests
import time
import sys

PROM_URL = "http://localhost:9090/api/v1/query"
API_URL = "http://localhost:3000/orders"


def query_prometheus(query):
    try:
        res = requests.get(PROM_URL, params={"query": query})
        return res.json()["data"]["result"]
    except Exception as e:
        print("❌ Prometheus query failed:", e)
        return []


def get_request_count():
    # 🔥 Don't over-filter → avoid missing labels
    query = 'http_server_duration_count'
    result = query_prometheus(query)

    total = 0
    for r in result:
        try:
            total += float(r["value"][1])
        except:
            pass

    return total


def run_test():
    print("\n=== METRICS VALIDATION ===\n")

    # Step 1
    before = get_request_count()
    print("Before count:", before)

    # Step 2: generate traffic
    print("Calling API...")
    for _ in range(5):
        try:
            requests.get(API_URL)
        except:
            pass

    # Step 3: wait for scrape (IMPORTANT)
    print("Waiting for Prometheus scrape...")
    time.sleep(15)

    # Step 4
    after = get_request_count()
    print("After count:", after)

    if after <= before:
        print("❌ METRIC DID NOT INCREASE")
        sys.exit(1)
    else:
        print("✅ METRIC COUNT INCREASED")

    # Step 5: error metric
    print("\nTriggering error...")
    for _ in range(2):
        try:
            requests.get(API_URL + "?fail=true")
        except:
            pass

    time.sleep(15)

    error_query = 'http_server_duration_count{http_status_code="500"}'
    errors = query_prometheus(error_query)

    if not errors:
        print("❌ ERROR METRIC NOT FOUND")
        sys.exit(1)
    else:
        print("✅ ERROR METRIC FOUND (500)")


if __name__ == "__main__":
    run_test()