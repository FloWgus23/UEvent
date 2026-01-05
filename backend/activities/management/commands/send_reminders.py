from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime, timedelta
from activities.models import Activity, Registration
from notifications.models import Notification

class Command(BaseCommand):
    help = 'ส่งการแจ้งเตือนกิจกรรม (ป้องกันการส่งซ้ำ)'

    def handle(self, *args, **kwargs):
        now = timezone.now()
        today = now.date()
        tomorrow = today + timedelta(days=1)
        count = 0

        # ==========================================
        # 1. แจ้งเตือนล่วงหน้า 1 วัน (24 ชั่วโมง)
        # ==========================================
        upcoming_activities = Activity.objects.filter(
            date=tomorrow
        ).exclude(status='สิ้นสุดแล้ว')

        for activity in upcoming_activities:
            regs = Registration.objects.filter(activity=activity)
            for reg in regs:
                # ⭐ แก้ไข: เช็คจาก Title + วันที่ (ตัด message__contains ออกเพราะทำให้บั๊ก)
                already_sent_today = Notification.objects.filter(
                    recipient=reg.user,
                    title=f"⏳ พรุ่งนี้แล้ว! กิจกรรม {activity.name}", # เช็คชื่อกิจกรรมในหัวข้อเลย
                    created_at__date=today # เช็คว่า "วันนี้" ส่งไปหรือยัง
                ).exists()

                if not already_sent_today:
                    Notification.objects.create(
                        recipient=reg.user,
                        title=f"⏳ พรุ่งนี้แล้ว! กิจกรรม {activity.name}",
                        message=f"กิจกรรมจะเริ่มในวันพรุ่งนี้ เวลา {activity.start_time.strftime('%H:%M') if activity.start_time else '-'} ณ {activity.location}",
                        notification_type='warning'
                    )
                    count += 1
                    self.stdout.write(f"   -> ส่งเตือนล่วงหน้าให้ {reg.user.username}")

        # ==========================================
        # 2. แจ้งเตือนด่วน (ก่อนเริ่ม 30 นาที)
        # ==========================================
        today_activities = Activity.objects.filter(
            date=today
        ).exclude(status='สิ้นสุดแล้ว')

        for activity in today_activities:
            if not activity.start_time:
                continue

            # คำนวณเวลา
            activity_datetime = datetime.combine(activity.date, activity.start_time)
            if timezone.is_naive(activity_datetime):
                activity_datetime = timezone.make_aware(activity_datetime)
            
            time_diff = activity_datetime - now

            # ถ้าเหลือเวลา 0 - 30 นาที
            if timedelta(minutes=0) < time_diff <= timedelta(minutes=30):
                regs = Registration.objects.filter(activity=activity)
                for reg in regs:
                    # ⭐ แก้ไข: เช็คแบบเดียวกัน
                    already_sent_urgent = Notification.objects.filter(
                        recipient=reg.user,
                        title=f"⏰ อีก 30 นาที! กิจกรรม {activity.name}",
                        created_at__date=today
                    ).exists()

                    if not already_sent_urgent:
                        Notification.objects.create(
                            recipient=reg.user,
                            title=f"⏰ อีก 30 นาที! กิจกรรม {activity.name}",
                            message=f"เตรียมตัวให้พร้อม! กิจกรรมจะเริ่มเวลา {activity.start_time.strftime('%H:%M')} น.",
                            notification_type='warning'
                        )
                        count += 1
                        self.stdout.write(f"   -> ส่งเตือนด่วนให้ {reg.user.username}")

        self.stdout.write(self.style.SUCCESS(f'✅ ตรวจสอบเสร็จสิ้น ส่งแจ้งเตือนไปทั้งหมด: {count} รายการ'))