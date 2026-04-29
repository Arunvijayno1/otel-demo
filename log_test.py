import requests
import time

API_URL = "http://localhost:3000/orders"
LOG_FILE = "app.log"

print("=== LOG CORRELATION VALIDATION ===")

# Call API
res = requests.get(API_URL)
print("API Status:", res.status_code)

time.sleep(2)

# Read logs
with open(LOG_FILE, "r") as f:
    logs = f.read()

if "trace_id" in logs:
    print("✅ trace_id found in logs")
    print("🎉 LOG CORRELATION PASSED")
else:
    print("❌ trace_id NOT found")
    exit(1)