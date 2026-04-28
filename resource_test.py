import requests
import time

JAEGER_URL = "http://localhost:16686/api/traces?service=order-service&limit=10&lookback=1m"

def validate_resource_attributes():
    res = requests.get(JAEGER_URL).json()

    for trace in res.get("data", []):
        processes = trace.get("processes", {})

        for process_id, process in processes.items():
            for tag in process.get("tags", []):
                if tag["key"] == "deployment.environment" and tag["value"] == "dev":
                    print("✅ deployment.environment = dev found")
                    return True

    return False

if __name__ == "__main__":
    time.sleep(3)
    if validate_resource_attributes():
        print("🎉 RESOURCE ATTRIBUTE VALIDATION PASSED")
    else:
        print("❌ RESOURCE ATTRIBUTE VALIDATION FAILED")