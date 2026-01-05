# backend/activities/signals.py

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Registration, Activity
# ตรวจสอบ path import ของ Notification ให้ตรงกับโปรเจคของคุณ
try:
    from notifications.models import Notification
except ImportError:
    # เผื่อกรณีรัน migrate ครั้งแรกแล้วยังไม่มี table
    Notification = None

@receiver(post_save, sender=Registration)
def create_registration_notification(sender, instance, created, **kwargs):
    """
    เมื่อมีการลงทะเบียนกิจกรรม (Registration Created)
    ให้สร้าง Notification ไปหา User คนนั้น
    """
    if created and Notification:
        Notification.objects.create(
            recipient=instance.user,
            title="ลงทะเบียนสำเร็จ! 🎉",
            message=f"คุณได้ลงทะเบียนเข้าร่วม '{instance.activity.name}' เรียบร้อยแล้ว",
            notification_type='success'
        )

# ⭐ เพิ่มส่วนนี้: แจ้งเตือนเมื่อมีการแก้ไขกิจกรรม (Pre-save เพื่อเทียบข้อมูลเก่ากับใหม่)
@receiver(pre_save, sender=Activity)
def activity_change_notification(sender, instance, **kwargs):
    if not instance.pk or not Notification:
        return

    try:
        # ดึงข้อมูลเก่าจาก Database
        old_activity = Activity.objects.get(pk=instance.pk)
        
        # ดึงรายชื่อคนลงทะเบียนทั้งหมด
        registrations = Registration.objects.filter(activity=instance)
        recipients = [reg.user for reg in registrations]

        if not recipients:
            return

        # 1. กรณี: เปลี่ยนสถานะเป็น 'สิ้นสุดแล้ว' (หรือถูกยกเลิก ถ้ามี status นี้)
        if old_activity.status != instance.status and instance.status == 'สิ้นสุดแล้ว':
            for user in recipients:
                Notification.objects.create(
                    recipient=user,
                    title=f"🏁 กิจกรรมสิ้นสุด/ยุติ: {instance.name}",
                    message="กิจกรรมนี้ได้สิ้นสุดลงหรือถูกยุติการจัดแล้ว กรุณาตรวจสอบสถานะ",
                    notification_type='warning'
                )

        # 2. กรณี: เลื่อนวันหรือเวลา
        elif old_activity.date != instance.date or old_activity.start_time != instance.start_time:
            old_date_str = old_activity.date.strftime('%d/%m/%Y')
            new_date_str = instance.date.strftime('%d/%m/%Y')
            
            for user in recipients:
                Notification.objects.create(
                    recipient=user,
                    title=f"📅 แจ้งเลื่อนกิจกรรม: {instance.name}",
                    message=f"มีการเปลี่ยนแปลงวัน/เวลา จาก {old_date_str} เป็น {new_date_str} กรุณาตรวจสอบข้อมูลใหม่",
                    notification_type='info'
                )

        # 3. กรณี: เปลี่ยนสถานที่
        elif old_activity.location != instance.location:
             for user in recipients:
                Notification.objects.create(
                    recipient=user,
                    title=f"📍 เปลี่ยนสถานที่: {instance.name}",
                    message=f"กิจกรรมย้ายสถานที่ไปยัง: {instance.location}",
                    notification_type='info'
                )

    except Activity.DoesNotExist:
        pass