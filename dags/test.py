from datetime import datetime, date, timezone, timedelta

KST = timezone(timedelta(hours=9))
time_record = datetime.now(KST).strftime("%Y%m%d")

print(time_record)