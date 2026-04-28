import requests
import time

JAEGER_URL = "http://localhost:16686/api/traces?service=order-service"
API_URL = "http://localhost:3000/test-trace"

def get_trace_count():
    try:
        res = requests.get(JAEGER_URL)
        return len(res.json().get("data", []))
    except:
        return 0

print("Calling API...")
requests.get(API_URL)

print("Waiting for traces (retry)...")

max_retries = 10
for i in range(max_retries):
    time.sleep(2)
    
    count = get_trace_count()
    print(f"Attempt {i+1}: traces = {count}")

    if count > 0:
        print("✅ TRACE VALIDATION PASSED")
        exit(0)

print("❌ TRACE VALIDATION FAILED (no traces after retries)")
exit(1)