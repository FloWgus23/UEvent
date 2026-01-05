import os
import django

# ⭐ สำคัญ: ถ้าโปรเจกต์คุณชื่ออื่นที่ไม่ใช่ 'uevent' ให้แก้ตรงนี้
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'uevent.settings')
django.setup()

from activities.models import Tag

# ข้อมูล Tags 40 รายการ (ภาษาไทย + Icon + สี)
TAGS_DATA = [
    # 🎓 หมวดวิชาการ
    {'id': 1, 'name': 'เขียนโปรแกรม', 'icon': '💻', 'color': '#3B82F6'},
    {'id': 2, 'name': 'AI และข้อมูล', 'icon': '🤖', 'color': '#6366F1'},
    {'id': 3, 'name': 'นวัตกรรม', 'icon': '💡', 'color': '#F59E0B'},
    {'id': 4, 'name': 'วิทยาศาสตร์', 'icon': '🔬', 'color': '#10B981'},
    {'id': 5, 'name': 'ออกแบบ', 'icon': '🎨', 'color': '#EC4899'},
    {'id': 6, 'name': 'สื่อ/มีเดีย', 'icon': '🎬', 'color': '#EF4444'},
    {'id': 7, 'name': 'ภาษา', 'icon': '🗣️', 'color': '#8B5CF6'},
    {'id': 8, 'name': 'ติวสอบ', 'icon': '📚', 'color': '#F97316'},

    # 💼 หมวดธุรกิจ & สังคม
    {'id': 9, 'name': 'บริหารธุรกิจ', 'icon': '💼', 'color': '#64748B'},
    {'id': 10, 'name': 'การตลาด', 'icon': '📈', 'color': '#F59E0B'},
    {'id': 11, 'name': 'การเงิน/หุ้น', 'icon': '💰', 'color': '#EAB308'},
    {'id': 12, 'name': 'สตาร์ทอัพ', 'icon': '🚀', 'color': '#10B981'},
    {'id': 13, 'name': 'หางาน/ฝึกงาน', 'icon': '👔', 'color': '#4B5563'},
    {'id': 14, 'name': 'กฎหมาย/สังคม', 'icon': '⚖️', 'color': '#1F2937'},
    {'id': 15, 'name': 'ภาวะผู้นำ', 'icon': '🏆', 'color': '#7C3AED'},
    {'id': 16, 'name': 'เสวนา/บรรยาย', 'icon': '🎙️', 'color': '#0EA5E9'},

    # 🧘‍♂️ หมวดสุขภาพ
    {'id': 17, 'name': 'สุขภาพ', 'icon': '🩺', 'color': '#EF4444'},
    {'id': 18, 'name': 'สุขภาพจิต', 'icon': '🧠', 'color': '#F472B6'},
    {'id': 19, 'name': 'กีฬา', 'icon': '⚽', 'color': '#22C55E'},
    {'id': 20, 'name': 'วิ่ง', 'icon': '🏃', 'color': '#F97316'},
    {'id': 21, 'name': 'ฟิตเนส', 'icon': '💪', 'color': '#14B8A6'},
    {'id': 22, 'name': 'เกษตร/ธรรมชาติ', 'icon': '🌱', 'color': '#16A34A'},

    # 🎉 หมวดบันเทิง
    {'id': 23, 'name': 'ดนตรี', 'icon': '🎵', 'color': '#EC4899'},
    {'id': 24, 'name': 'ภาพยนตร์', 'icon': '🍿', 'color': '#DC2626'},
    {'id': 25, 'name': 'ศิลปะ', 'icon': '🖌️', 'color': '#8B5CF6'},
    {'id': 26, 'name': 'ถ่ายภาพ', 'icon': '📷', 'color': '#374151'},
    {'id': 27, 'name': 'เกม', 'icon': '🎮', 'color': '#6366F1'},
    {'id': 28, 'name': 'บอร์ดเกม', 'icon': '🎲', 'color': '#F59E0B'},
    {'id': 29, 'name': 'ท่องเที่ยว', 'icon': '✈️', 'color': '#0EA5E9'},
    {'id': 30, 'name': 'อาหาร', 'icon': '🍔', 'color': '#F97316'},
    {'id': 31, 'name': 'แฟชั่น', 'icon': '👗', 'color': '#DB2777'},
    {'id': 32, 'name': 'สัตว์เลี้ยง', 'icon': '🐶', 'color': '#A855F7'},
    {'id': 33, 'name': 'มูเตลู', 'icon': '🔮', 'color': '#7C3AED'},

    # 🤝 หมวดกิจกรรม
    {'id': 34, 'name': 'จิตอาสา', 'icon': '🤝', 'color': '#3B82F6'},
    {'id': 35, 'name': 'ค่ายอาสา', 'icon': '⛺', 'color': '#16A34A'},
    {'id': 36, 'name': 'สิ่งแวดล้อม', 'icon': '♻️', 'color': '#10B981'},
    {'id': 37, 'name': 'รับน้อง', 'icon': '🎉', 'color': '#F43F5E'},
    {'id': 38, 'name': 'วัฒนธรรม', 'icon': '🙏', 'color': '#D97706'},
    {'id': 39, 'name': 'เวิร์กชอป', 'icon': '🛠️', 'color': '#F59E0B'},
    {'id': 40, 'name': 'การแข่งขัน', 'icon': '🥇', 'color': '#EAB308'}
]

def seed():
    print("🌱 เริ่มต้นการอัปเดตข้อมูล Tags...")
    
    count_created = 0
    count_updated = 0
    
    for data in TAGS_DATA:
        # ใช้ update_or_create เพื่อแก้ของเก่าหรือสร้างใหม่ถ้ายังไม่มี
        tag, created = Tag.objects.update_or_create(
            id=data['id'],  # ยึดตาม ID เป็นหลักเพื่อให้ตรงกับ Frontend
            defaults={
                'name': data['name'],
                'icon': data['icon'],
                'color': data['color'],
                'is_active': True
            }
        )
        
        if created:
            count_created += 1
            print(f"✅ สร้างใหม่: {tag.name} {tag.icon}")
        else:
            count_updated += 1
            print(f"🔄 อัปเดต: {tag.name} {tag.icon}")
            
    print(f"\n🎉 เสร็จสิ้น! สร้างใหม่: {count_created}, อัปเดต: {count_updated}")

if __name__ == '__main__':
    seed()