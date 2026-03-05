# backend/users/signals.py
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import UserProfile
from django.core.mail import send_mail  # <--- เพิ่มอันนี้
from django_rest_passwordreset.signals import reset_password_token_created # <--- และอันนี้

# import model Notification (อ้างอิงจากโค้ด activities/signals.py ของคุณ)
try:
    from notifications.models import Notification
except ImportError:
    Notification = None

# ==========================================
# ส่วนที่ 1: แอบดูสถานะเก่า (Pre-Save)
# ==========================================

@receiver(pre_save, sender=UserProfile)
def track_previous_status(sender, instance, **kwargs):
    """
    เก็บสถานะเก่าไว้ก่อนบันทึก เพื่อเช็คว่ามีการเปลี่ยนแปลงหรือไม่
    """
    try:
        old_instance = UserProfile.objects.get(pk=instance.pk)
        instance._previous_status = old_instance.organizer_status
    except UserProfile.DoesNotExist:
        instance._previous_status = None

# ==========================================
# ส่วนที่ 2: แจ้งเตือนผลอนุมัติ (Post-Save)
# ==========================================

@receiver(post_save, sender=UserProfile)
def send_organizer_status_notification(sender, instance, created, **kwargs):
    """
    แจ้งเตือนเมื่อสถานะผู้จัด (organizer_status) เปลี่ยนแปลง
    """
    if created or Notification is None:
        return

    previous_status = getattr(instance, '_previous_status', None)
    current_status = instance.organizer_status

    # ถ้าสถานะเปลี่ยน
    if previous_status != current_status:
        
        # ✅ กรณี: อนุมัติ (Approved)
        if current_status == 'approved':
            Notification.objects.create(
                recipient=instance.user,  # ⭐ แก้เป็น recipient ตามระบบเดิมของคุณ
                title="คำขอเป็นผู้จัดได้รับการอนุมัติ 🎉",
                message="ยินดีด้วย! คุณได้รับการอนุมัติเป็นผู้จัดกิจกรรมแล้ว สามารถเริ่มสร้างกิจกรรมได้ทันที",
                notification_type='success'
            )
        
        # ❌ กรณี: ไม่อนุมัติ (Rejected)
        elif current_status == 'rejected':
            Notification.objects.create(
                recipient=instance.user,  # ⭐ แก้เป็น recipient
                title="คำขอเป็นผู้จัดไม่ผ่านการอนุมัติ ⚠️",
                message="กรุณาตรวจสอบเอกสารและยื่นคำขอใหม่อีกครั้ง หรือติดต่อผู้ดูแลระบบ",
                notification_type='warning'
            )


#ลืมรหัสผ่าน
@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    """
    ทำงานเมื่อมีการสร้าง Token สำหรับรีเซ็ตรหัสผ่าน
    """
    # 1. สร้าง Link (สมมติว่า Frontend รันที่ Port 5173)
    # ถ้าขึ้น Production ต้องเปลี่ยน localhost เป็นชื่อเว็บจริง
    link = f"http://localhost:5173/forgot-password?token={reset_password_token.key}"

    # 2. (สำหรับ Dev) ปริ้นท์ลงจอดำ Terminal เพื่อให้เราก๊อปไปใช้ได้เลย
    print("\n" + "="*50)
    print(f"🔑 PASSWORD RESET LINK: {link}")
    print("="*50 + "\n")

    # 3. ส่งอีเมลจริง (ถ้าตั้งค่า ConsoleBackend ไว้ มันก็จะโชว์ใน Terminal เหมือนกัน)
    email_subject = "Reset your password for UEvent"
    email_message = f"Click the link below to reset your password:\n{link}"
    
    send_mail(
        email_subject,
        email_message,
        "noreply@uevent.com", # อีเมลผู้ส่ง (ตั้งมั่วๆ ไปก่อนได้ถ้าเทสในเครื่อง)
        [reset_password_token.user.email]
    )