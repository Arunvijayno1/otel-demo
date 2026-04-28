import requests
import time

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
    query = 'http_server_duration_count{http_route="/orders"}'
    result = query_prometheus(query)

    total = 0
    for r in result:
        total += float(r["value"][1])

    return total


def run_test():
    print("\n=== METRICS VALIDATION ===\n")

    # Step 1: Get initial count
    before = get_request_count()
    print("Before count:", before)

    # Step 2: Call API multiple times
    print("Calling API...")
    for _ in range(3):
        requests.get(API_URL)

    # Step 3: Wait for scrape
    print("Waiting for Prometheus scrape...")
    time.sleep(5)

    # Step 4: Get new count
    after = get_request_count()
    print("After count:", after)

    # Step 5: Validate increase
    if after > before:
        print("✅ METRIC COUNT INCREASED")
    else:
        print("❌ METRIC DID NOT INCREASE")

    # Step 6: Validate error metric
    print("\nTriggering error...")
    requests.get(API_URL + "?fail=true")

    time.sleep(5)

    error_query = 'http_server_duration_count{http_route="/orders",http_status_code="500"}'
    errors = query_prometheus(error_query)

    if errors:
        print("✅ ERROR METRIC FOUND (500)")
    else:
        print("❌ ERROR METRIC NOT FOUND")


if __name__ == "__main__":
    run_test()