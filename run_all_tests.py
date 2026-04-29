# run_all_tests.py

import os

tests = [
    "trace_test.py",
    "metrics_test.py",
    "resource_test.py",
    "log_test.py"
]

for test in tests:
    print(f"\nRunning {test}...")
    result = os.system(f"python {test}")

    if result != 0:
        print(f"❌ {test} FAILED")
        exit(1)

print("\n🎉 ALL TESTS PASSED")