"""Posting slots for a week starting Monday <YYYY-MM-DD>, as IST ISO strings.
Shorts: 07:00 America/New_York every day. Long videos: 20:00 America/New_York on Monday (long1, prayer), Thursday (long2, prayer)
and Saturday (long3, Bible story).
python3 slots.py 2026-10-26
"""
import json, sys
from datetime import date, datetime, time, timedelta
from zoneinfo import ZoneInfo
ET, IST = ZoneInfo("America/New_York"), ZoneInfo("Asia/Kolkata")
mon = date.fromisoformat(sys.argv[1])
def ist(d, hh):
    return datetime.combine(d, time(hh, 0), ET).astimezone(IST).strftime("%Y-%m-%dT%H:%M:%S")
# Shorts post at 07:00 ET on the same calendar day as the IST date (Mon-Sun)
shorts = [ist(mon + timedelta(days=i), 7) for i in range(7)]
longs = {"long1": ist(mon, 20), "long2": ist(mon + timedelta(days=3), 20), "long3": ist(mon + timedelta(days=5), 20)}
print(json.dumps({"shorts": shorts, **longs}, indent=1))
