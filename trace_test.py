import requests
import time

API_URL = "http://localhost:3000/orders"
JAEGER_URL = "http://localhost:16686/api/traces?service=order-service&lookback=1m&limit=10"
LOG_FILE = "app.log"


# Step 1: Call API
def call_api():
    try:
        res = requests.get(API_URL)
        print("API Status:", res.status_code)
        return res.status_code == 200
    except Exception as e:
        print("❌ API call failed:", e)
        return False


# Step 2: Get traces
def get_traces():
    try:
        res = requests.get(JAEGER_URL, timeout=5)
        return res.json().get("data", [])
    except Exception as e:
        print("❌ Jaeger not reachable:", e)
        return []


# Step 3: Extract trace_id
def extract_trace_id(traces):
    for trace in traces:
        for span in trace.get("spans", []):
            if span.get("operationName") == "GET /orders":
                trace_id = trace.get("traceID")
                print("✅ Found trace_id:", trace_id)
                return trace_id
    return None


# Step 4: Check logs for trace_id
def check_log_for_trace(trace_id):
    try:
        with open(LOG_FILE, "r") as file:
            logs = file.read()

        if trace_id in logs:
            print("✅ trace_id found in logs → CORRELATED")
            return True
        else:
            print("❌ trace_id NOT found in logs")
            return False

    except FileNotFoundError:
        print("❌ app.log not found")
        return False


# Step 5: Run validation
def run_test():
    print("\n=== LOG CORRELATION VALIDATION ===\n")

    # Call API
    if not call_api():
        return False

    # Wait for trace + log write
    time.sleep(5)

    # Get traces
    traces = get_traces()
    if not traces:
        print("❌ No traces found")
        return False

    # Extract trace_id
    trace_id = extract_trace_id(traces)
    if not trace_id:
        print("❌ No valid trace found")
        return False

    # Validate logs
    log_ok = check_log_for_trace(trace_id)

    if log_ok:
        print("\n🎉 LOG CORRELATION PASSED")
        return True
    else:
        print("\n❌ LOG CORRELATION FAILED")
        return False


if __name__ == "__main__":
    success = run_test()
    exit(0 if success else 1)