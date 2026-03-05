import time
import subprocess
from datetime import datetime

#ระบบแจ้งเตือนอัตโนมัติ
# ตั้งค่า: จะให้เช็คทุกๆ กี่วินาที (แนะนำ 60 วินาที = 1 นาที)
INTERVAL = 60 

print("🚀 เริ่มต้นระบบแจ้งเตือนอัตโนมัติ (Scheduler started)...")
print(f"⏳ ระบบจะตรวจสอบทุกๆ {INTERVAL} วินาที")
print("-" * 30)

try:
    while True:
        now = datetime.now().strftime("%H:%M:%S")
        print(f"[{now}] 🔍 กำลังตรวจสอบกิจกรรม...")
        
        # สั่งรันคำสั่ง manage.py send_reminders
        # shell=True เพื่อให้รองรับคำสั่ง python ใน Windows/Mac
        subprocess.run(["python", "manage.py", "send_reminders"], shell=True)
        
        print(f"✅ ตรวจสอบเสร็จสิ้น รอรอบถัดไป...")
        print("-" * 30)
        
        # หยุดรอตามเวลาที่กำหนด
        time.sleep(INTERVAL)

except KeyboardInterrupt:
    print("\n🛑 หยุดการทำงานของระบบแจ้งเตือน")