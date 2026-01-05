# backend/activities/management/commands/update_activity_status.py

from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime
from activities.models import Activity

class Command(BaseCommand):
    help = 'ตรวจสอบและอัปเดตสถานะกิจกรรมที่สิ้นสุดแล้ว'

    def handle(self, *args, **kwargs):
        now = timezone.now()
        count = 0

        # ดึงกิจกรรมที่ยังไม่จบ (Exclude 'สิ้นสุดแล้ว' และ 'ยกเลิก')
        # ปรับ query นี้ให้ตรงกับ status choices ของคุณ
        active_activities = Activity.objects.exclude(status__in=['สิ้นสุดแล้ว', 'cancelled'])

        for activity in active_activities:
            should_close = False
            
            # กรณี 1: วันที่จัดกิจกรรม ผ่านมาแล้ว (เป็นเมื่อวาน หรือก่อนหน้านั้น)
            if activity.date < now.date():
                should_close = True
            
            # กรณี 2: วันนี้ แต่เวลาจบผ่านไปแล้ว
            elif activity.date == now.date() and activity.end_time:
                # รวมวันที่และเวลาจบเข้าด้วยกัน
                end_datetime = datetime.combine(activity.date, activity.end_time)
                if timezone.is_naive(end_datetime):
                    end_datetime = timezone.make_aware(end_datetime)
                
                if now > end_datetime:
                    should_close = True

            # ถ้าเข้าเงื่อนไข ให้เปลี่ยนสถานะ
            if should_close:
                activity.status = 'สิ้นสุดแล้ว' # หรือค่าที่คุณใช้ใน Model
                activity.save()
                count += 1
                self.stdout.write(f" -> ปิดกิจกรรม: {activity.name}")

        if count > 0:
            self.stdout.write(self.style.SUCCESS(f'✅ อัปเดตสถานะสำเร็จ: สิ้นสุดแล้ว {count} กิจกรรม'))
        else:
            self.stdout.write(self.style.SUCCESS('✨ ไม่มีกิจกรรมที่ต้องอัปเดต'))