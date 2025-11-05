import sys
from pathlib import Path
import httpx

base = "http://localhost:8000"

# 1) List videos
r = httpx.get(f"{base}/api/v1/videos", params={"limit": 10, "offset": 0})
print("LIST status:", r.status_code)
js = r.json()
print("total:", js.get("total"), "count:", js.get("count"))
items = js.get("items", [])
print("first item keys:", list(items[0].keys()) if items else [])

# 2) Detail (if any item exists)
if items:
    vid = items[0]["id"]
    r2 = httpx.get(f"{base}/api/v1/videos/{vid}")
    print("DETAIL status:", r2.status_code)
    j2 = r2.json()
    want_keys = [
        "id","file_path","file_hash","upload_date","duration_seconds","fps",
        "resolution","file_size_bytes","processing_status","training_date","training_type","location"
    ]
    print("detail has all keys:", all(k in j2 for k in want_keys))
    sample = {k:j2.get(k) for k in want_keys}
    print("sample detail:", sample)

# 3) Trigger scan POST (no-op incremental)
r3 = httpx.post(f"{base}/api/v1/videos/scan", json={"directory":"Midea","mode":"incremental"})
print("SCAN POST status:", r3.status_code)
print(r3.json())
