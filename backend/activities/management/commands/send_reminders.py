from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime, timedelta
from activities.models import Activity, Registration
from notifications.models import Notification

# ส่งการแจ้งเตือนอัตโนมัติ
class Command(BaseCommand):
    help = 'ส่งการแจ้งเตือนกิจกรรมตาม Timeline (ไม่ส่งซ้ำ)'

    def handle(self, *args, **kwargs):
        now = timezone.now()
        today = now.date()
        tomorrow = today + timedelta(days=1)
        count = 0

        # ==========================================
        # 1. แจ้งเตือนล่วงหน้า 1 วัน (24 ชั่วโมง)
        # ส่งเฉพาะผู้ที่ยังไม่เคยได้รับการแจ้งเตือน "พรุ่งนี้แล้ว"
        # ==========================================
        upcoming_activities = Activity.objects.filter(
            date=tomorrow
        ).exclude(status='สิ้นสุดแล้ว')

        for activity in upcoming_activities:
            regs = Registration.objects.filter(activity=activity)
            for reg in regs:
                # เช็คว่าเคยส่งการแจ้งเตือน "พรุ่งนี้แล้ว" ให้ user คนนี้สำหรับกิจกรรมนี้หรือยัง
                # (เช็คตลอดทั้งชีวิต ไม่ใช่แค่วันนี้)
                already_sent_tomorrow = Notification.objects.filter(
                    recipient=reg.user,
                    title__contains=f"พรุ่งนี้แล้ว! กิจกรรม {activity.name}"
                ).exists()

                if not already_sent_tomorrow:
                    Notification.objects.create(
                        recipient=reg.user,
                        title=f"⏳ พรุ่งนี้แล้ว! กิจกรรม {activity.name}",
                        message=f"กิจกรรมจะเริ่มในวันพรุ่งนี้ เวลา {activity.start_time.strftime('%H:%M') if activity.start_time else '-'} ณ {activity.location}",
                        notification_type='warning'
                    )
                    count += 1
                    self.stdout.write(f"   -> ส่งเตือนล่วงหน้าให้ {reg.user.username} (กิจกรรม: {activity.name})")

        # ==========================================
        # 2. แจ้งเตือนด่วน (ก่อนเริ่ม 30 นาที)
        # ส่งเฉพาะผู้ที่ยังไม่เคยได้รับการแจ้งเตือน "อีก 30 นาที"
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

            # ส่งเฉพาะเมื่อเหลือเวลา 25-35 นาที (ช่วง 10 นาที)
            if timedelta(minutes=25) <= time_diff <= timedelta(minutes=35):
                regs = Registration.objects.filter(activity=activity)
                for reg in regs:
                    # เช็คว่าเคยส่งการแจ้งเตือน "อีก 30 นาที" ให้ user คนนี้สำหรับกิจกรรมนี้หรือยัง
                    # (เช็คตลอดทั้งชีวิต ไม่ใช่แค่วันนี้)
                    already_sent_urgent = Notification.objects.filter(
                        recipient=reg.user,
                        title__contains=f"อีก 30 นาที! กิจกรรม {activity.name}"
                    ).exists()

                    if not already_sent_urgent:
                        Notification.objects.create(
                            recipient=reg.user,
                            title=f"⏰ อีก 30 นาที! กิจกรรม {activity.name}",
                            message=f"เตรียมตัวให้พร้อม! กิจกรรมจะเริ่มเวลา {activity.start_time.strftime('%H:%M')} น.",
                            notification_type='warning'
                        )
                        count += 1
                        self.stdout.write(f"   -> ส่งเตือนด่วนให้ {reg.user.username} (กิจกรรม: {activity.name})")

        if count > 0:
            self.stdout.write(self.style.SUCCESS(f'✅ ส่งแจ้งเตือนไปทั้งหมด: {count} รายการ'))
        else:
            self.stdout.write(self.style.SUCCESS('✨ ไม่มีการแจ้งเตือนที่ต้องส่ง'))