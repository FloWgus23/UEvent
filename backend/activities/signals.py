# backend/activities/signals.py

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Registration, Activity
from notifications.models import Notification

# ==========================================
# Signal 1: แจ้งเตือนเมื่อลงทะเบียน
# ==========================================
@receiver(post_save, sender=Registration)
def send_registration_notifications(sender, instance, created, **kwargs):
    """
    ส่งการแจ้งเตือนทันทีเมื่อมีการลงทะเบียนกิจกรรม
    จะตัดสินใจว่าควรส่งการแจ้งเตือนแบบไหนตามเวลาที่เหลือ
    """
    if not created:  # ถ้าไม่ใช่การสร้างใหม่ (แค่ update) ก็ไม่ทำอะไร
        return
    
    activity = instance.activity
    user = instance.user
    now = timezone.now()
    
    # ตรวจสอบว่ากิจกรรมสิ้นสุดหรือยกเลิกหรือยัง
    if activity.status in ['สิ้นสุดแล้ว', 'cancelled']:
        return
    
    # คำนวณระยะเวลาที่เหลือ
    activity_date = activity.date
    activity_start_time = activity.start_time
    
    if not activity_start_time:
        # ถ้าไม่มีเวลาเริ่ม ส่งแค่การแจ้งเตือนทั่วไป
        Notification.objects.create(
            recipient=user,
            title=f"🎉 ลงทะเบียนสำเร็จ! {activity.name}",
            message=f"คุณได้ลงทะเบียนกิจกรรมเรียบร้อยแล้ว วันที่ {activity_date.strftime('%d/%m/%Y')} ณ {activity.location}",
            notification_type='success'
        )
        return
    
    # รวมวันที่และเวลาเข้าด้วยกัน
    activity_datetime = datetime.combine(activity_date, activity_start_time)
    if timezone.is_naive(activity_datetime):
        activity_datetime = timezone.make_aware(activity_datetime)
    
    time_diff = activity_datetime - now
    
    # ==================================================================
    # กรณีที่ 1: ลงทะเบียนก่อนกิจกรรม 30 นาที - 2 ชั่วโมง
    # ส่งการแจ้งเตือนว่า "เตรียมตัวให้พร้อม"
    # ==================================================================
    if timedelta(minutes=30) <= time_diff <= timedelta(hours=2):
        Notification.objects.create(
            recipient=user,
            title=f"🎉 ลงทะเบียนสำเร็จ! {activity.name}",
            message=f"กิจกรรมจะเริ่มในอีก {int(time_diff.total_seconds() // 60)} นาที เวลา {activity_start_time.strftime('%H:%M')} น. ณ {activity.location} เตรียมตัวให้พร้อมนะ!",
            notification_type='success'
        )
        
    # ==================================================================
    # กรณีที่ 2: ลงทะเบียนภายใน 30 นาทีก่อนเริ่ม
    # ส่งการแจ้งเตือนด่วน
    # ==================================================================
    elif timedelta(minutes=0) < time_diff < timedelta(minutes=30):
        Notification.objects.create(
            recipient=user,
            title=f"⏰ รีบเลย! กิจกรรม {activity.name}",
            message=f"กิจกรรมจะเริ่มในอีก {int(time_diff.total_seconds() // 60)} นาที! เวลา {activity_start_time.strftime('%H:%M')} น. ณ {activity.location}",
            notification_type='warning'
        )
        
    # ==================================================================
    # กรณีที่ 3: ลงทะเบียนล่วงหน้ามากกว่า 2 ชั่วโมง
    # ส่งการแจ้งเตือนทั่วไป (ระบบจะส่งการแจ้งเตือนอื่นๆ ตาม schedule)
    # ==================================================================
    else:
        days_left = (activity_date - now.date()).days
        
        if days_left >= 1:
            Notification.objects.create(
                recipient=user,
                title=f"🎉 ลงทะเบียนสำเร็จ! {activity.name}",
                message=f"คุณได้ลงทะเบียนกิจกรรมเรียบร้อยแล้ว กิจกรรมจะเริ่มในวันที่ {activity_date.strftime('%d/%m/%Y')} เวลา {activity_start_time.strftime('%H:%M')} น. ณ {activity.location}",
                notification_type='success'
            )
        else:
            # วันเดียวกัน แต่ยังนานมาก
            Notification.objects.create(
                recipient=user,
                title=f"🎉 ลงทะเบียนสำเร็จ! {activity.name}",
                message=f"กิจกรรมวันนี้! เวลา {activity_start_time.strftime('%H:%M')} น. ณ {activity.location}",
                notification_type='success'
            )


# ==========================================
# Signal 2: แจ้งเตือนเมื่อมีการแก้ไขกิจกรรม
# ==========================================

# เก็บค่าเดิมของ Activity ก่อนบันทึก
@receiver(pre_save, sender=Activity)
def store_old_activity_data(sender, instance, **kwargs):
    """
    เก็บข้อมูลเดิมของกิจกรรมก่อนการแก้ไข
    """
    if instance.pk:  # ถ้ามี pk แสดงว่าเป็นการ update ไม่ใช่การสร้างใหม่
        try:
            old_activity = Activity.objects.get(pk=instance.pk)
            # เก็บค่าเดิมไว้ใน instance
            instance._old_date = old_activity.date
            instance._old_start_time = old_activity.start_time
            instance._old_end_time = old_activity.end_time
            instance._old_location = old_activity.location
            instance._old_status = old_activity.status
        except Activity.DoesNotExist:
            pass


@receiver(post_save, sender=Activity)
def send_activity_update_notifications(sender, instance, created, **kwargs):
    """
    ส่งการแจ้งเตือนเมื่อมีการเปลี่ยนแปลงกิจกรรม
    """
    # ถ้าเป็นการสร้างใหม่ ไม่ต้องแจ้งเตือน
    if created:
        return
    
    # ตรวจสอบว่ามีการเปลี่ยนแปลงหรือไม่
    has_changes = False
    changes_list = []
    
    # เช็คการเปลี่ยนแปลงวันที่
    if hasattr(instance, '_old_date') and instance._old_date != instance.date:
        has_changes = True
        old_date_str = instance._old_date.strftime('%d/%m/%Y')
        new_date_str = instance.date.strftime('%d/%m/%Y')
        changes_list.append(f"📅 วันที่: {old_date_str} → {new_date_str}")
    
    # เช็คการเปลี่ยนแปลงเวลาเริ่ม
    if hasattr(instance, '_old_start_time') and instance._old_start_time != instance.start_time:
        has_changes = True
        old_time = instance._old_start_time.strftime('%H:%M') if instance._old_start_time else '-'
        new_time = instance.start_time.strftime('%H:%M') if instance.start_time else '-'
        changes_list.append(f"🕐 เวลาเริ่ม: {old_time} → {new_time} น.")
    
    # เช็คการเปลี่ยนแปลงเวลาจบ
    if hasattr(instance, '_old_end_time') and instance._old_end_time != instance.end_time:
        has_changes = True
        old_time = instance._old_end_time.strftime('%H:%M') if instance._old_end_time else '-'
        new_time = instance.end_time.strftime('%H:%M') if instance.end_time else '-'
        changes_list.append(f"🕐 เวลาจบ: {old_time} → {new_time} น.")
    
    # เช็คการเปลี่ยนแปลงสถานที่
    if hasattr(instance, '_old_location') and instance._old_location != instance.location:
        has_changes = True
        changes_list.append(f"📍 สถานที่: {instance._old_location} → {instance.location}")
    
    # เช็คการยกเลิกกิจกรรม
    if hasattr(instance, '_old_status') and instance._old_status != instance.status:
        if instance.status == 'cancelled' or instance.status == 'ยกเลิก':
            # ส่งการแจ้งเตือนพิเศษสำหรับการยกเลิก
            registrations = Registration.objects.filter(activity=instance)
            for reg in registrations:
                Notification.objects.create(
                    recipient=reg.user,
                    title=f"❌ กิจกรรมถูกยกเลิก: {instance.name}",
                    message=f"ขออภัย! กิจกรรม '{instance.name}' ได้ถูกยกเลิก เราจะแจ้งให้ทราบเมื่อมีกิจกรรมใหม่",
                    notification_type='error'
                )
            return  # จบการทำงานเพราะส่งการแจ้งเตือนยกเลิกแล้ว
    
    # ถ้ามีการเปลี่ยนแปลง ส่งการแจ้งเตือนให้ผู้ลงทะเบียน
    if has_changes:
        changes_text = "\n".join(changes_list)
        registrations = Registration.objects.filter(activity=instance)
        
        for reg in registrations:
            Notification.objects.create(
                recipient=reg.user,
                title=f"⚠️ มีการเปลี่ยนแปลง! {instance.name}",
                message=f"กิจกรรม '{instance.name}' มีการเปลี่ยนแปลง:\n\n{changes_text}\n\nกรุณาตรวจสอบรายละเอียดใหม่",
                notification_type='warning'
            )