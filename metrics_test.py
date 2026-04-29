import requests
import time
import sys

PROM_URL = "http://localhost:9090/api/v1/query"
API_URL = "http://localhost:3000/orders"


def query_prometheus(query):
    try:
        res = requests.get(PROM_URL, params={"query": query})
        data = res.json()
        return data.get("data", {}).get("result", [])
    except Exception as e:
        print("❌ Prometheus query failed:", e)
        return []


def get_request_count():
    query = 'http_server_duration_count{http_route="/orders"}'
    result = query_prometheus(query)

    total = 0
    for r in result:
        total += float(r["value"][1])

    return total


def run_test():
    print("\n=== METRICS VALIDATION ===\n")

    # STEP 1: Initial value
    before = get_request_count()
    print("Before count:", before)

    # STEP 2: Generate traffic
    print("Calling API...")
    for _ in range(5):
        requests.get(API_URL)

    # STEP 3: Retry scrape wait
    print("Waiting for Prometheus scrape (retry)...")

    after = before
    for i in range(10):
        time.sleep(2)
        after = get_request_count()
        print(f"Attempt {i+1}: count = {after}")

        if after > before:
            break

    # STEP 4: Validate
    if after > before:
        print("✅ METRIC COUNT INCREASED")
    else:
        print("❌ METRIC DID NOT INCREASE")
        sys.exit(1)

    # STEP 5: Error metric
    print("\nTriggering error...")
    requests.get(API_URL + "?fail=true")

    time.sleep(5)

    error_query = 'http_server_duration_count{http_route="/orders",http_status_code="500"}'
    errors = query_prometheus(error_query)

    if errors:
        print("✅ ERROR METRIC FOUND (500)")
    else:
        print("❌ ERROR METRIC NOT FOUND")
        sys.exit(1)


if __name__ == "__main__":
    run_test()