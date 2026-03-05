# backend/activities/serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from decimal import Decimal  # <--- เพิ่ม Import นี้
from .models import Activity, Registration, Tag, UserInterest, ActivityTag


# ========================================
# 🆕 TAG SYSTEM SERIALIZERS
# ========================================

# แท็ก
class TagSerializer(serializers.ModelSerializer):
    """Serializer สำหรับ Tag"""
    class Meta:
        model = Tag
        fields = ['id', 'name', 'icon', 'description', 'color', 'is_active']
        read_only_fields = ['id']


#ความสนใจของผู้ใช้
class UserInterestSerializer(serializers.ModelSerializer):
    """Serializer สำหรับแสดงความสนใจของผู้ใช้"""
    tag = TagSerializer(read_only=True)
    tag_id = serializers.IntegerField(write_only=True)
    total_score = serializers.ReadOnlyField()
    
    class Meta:
        model = UserInterest
        fields = [
            'id', 'tag', 'tag_id', 'explicit_score', 
            'implicit_score', 'total_score', 'last_updated'
        ]
        read_only_fields = ['id', 'last_updated']


# สร้าง ผู้ใช้ใหม่จากการเลือกในหน้า Modal
class UserInterestCreateSerializer(serializers.Serializer):
    """
    Serializer สำหรับสร้าง UserInterest จาก Modal
    Input: {"tag_id": 1, "score": 5.0}
    """
    tag_id = serializers.IntegerField()
    
    # ⭐ แก้ไข: ใช้ Decimal(...) แทน float เพื่อความแม่นยำและแก้ Warning
    score = serializers.DecimalField(
        max_digits=5, 
        decimal_places=2,
        min_value=Decimal('0.0'),
        max_value=Decimal('10.0'),
        default=Decimal('5.0')  #เพราะว่าค่า Default ที่เราตั้งไว้ใน Onboarding.vue คือ 5.00
    )
    
    def validate_tag_id(self, value):
        """ตรวจสอบว่า Tag มีอยู่จริง"""
        if not Tag.objects.filter(id=value, is_active=True).exists():
            raise serializers.ValidationError(f"Tag ID {value} ไม่พบหรือไม่ได้ใช้งาน")
        return value


#รองรับการเลือกแท็กหลายตัวในหน้า Onboarding 
class BulkUserInterestCreateSerializer(serializers.Serializer):
    """
    Serializer สำหรับรับ Tags หลายตัวจาก Onboarding Modal
    Input: {"tags": [{"tag_id": 1, "score": 5.0}, ...]}
    """
    tags = UserInterestCreateSerializer(many=True)
    
    def validate_tags(self, value):
        """ตรวจสอบว่ามีอย่างน้อย 1 tag"""
        if not value:
            raise serializers.ValidationError("กรุณาเลือกอย่างน้อย 1 ความสนใจ")
        return value
    
    def create(self, validated_data):
        """สร้าง/อัพเดท UserInterest"""
        user = self.context['request'].user
        tags_data = validated_data['tags']
        
        created_interests = []
        
        for tag_data in tags_data:
            try:
                tag = Tag.objects.get(id=tag_data['tag_id'])
                
                interest, created = UserInterest.objects.update_or_create(
                    user=user,
                    tag=tag,
                    defaults={'explicit_score': tag_data['score']}
                )
                
                created_interests.append(interest)
                print(f"{'✅ Created' if created else '🔄 Updated'}: {interest}")
                
            except Tag.DoesNotExist:
                # Skip invalid tags
                print(f"⚠️ Tag ID {tag_data['tag_id']} not found, skipping...")
                continue
            except Exception as e:
                print(f"❌ Error creating interest for tag {tag_data['tag_id']}: {e}")
                continue
        
        return created_interests


# ========================================
# EXISTING SERIALIZERS (ปรับปรุง)
# ========================================

#โปรไฟล์
class UserProfileSerializer(serializers.ModelSerializer):
    fullname = serializers.SerializerMethodField()
    phone = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'fullname', 'phone']

    def get_fullname(self, obj):
        full_name = f"{obj.first_name} {obj.last_name}".strip()
        return full_name if full_name else obj.username

    def get_phone(self, obj):
        try:
            if hasattr(obj, 'profile') and hasattr(obj.profile, 'phone'):
                return obj.profile.phone
        except:
            pass
        return ""


#ข้อมูลกิจกรรม
class ActivitySerializer(serializers.ModelSerializer):
    """Serializer สำหรับแสดงข้อมูลกิจกรรม"""
    registration_status = serializers.ReadOnlyField()
    time_display = serializers.ReadOnlyField()
    image = serializers.SerializerMethodField()
    
    # 🆕 เพิ่ม tag_list
    tag_list = TagSerializer(many=True, read_only=True)
    
    # 🆕 เพิ่ม owner_id เพื่อให้ Frontend เช็คได้
    owner_id = serializers.IntegerField(source='owner.id', read_only=True, allow_null=True)
    
    class Meta:
        model = Activity
        fields = [
            'id', 'name', 'description', 'date', 'start_time', 'end_time',
            'time_display', 'capacity', 'location', 'organizer', 'tags', 
            'tag_list',  # 🆕 เพิ่ม
            'category', 'image', 'registered_count', 'status', 
            'registration_status', 'owner_id', 'created_at', 'updated_at'  # 🆕 เพิ่ม owner_id
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'registered_count', 'status', 'owner_id']
    
    def get_image(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request is not None:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None


#สร้างกิจกรรม
class ActivityCreateSerializer(serializers.ModelSerializer):
    """Serializer สำหรับสร้างกิจกรรมใหม่"""
    
    tags = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    
    # 🆕 รับ tag_ids เป็น list
    tag_ids = serializers.ListField(
        child=serializers.IntegerField(),
        required=False,
        write_only=True
    )
    
    image = serializers.ImageField(required=False, allow_null=True)
    start_time = serializers.TimeField(required=False, allow_null=True, format='%H:%M')
    end_time = serializers.TimeField(required=False, allow_null=True, format='%H:%M')
    
    class Meta:
        model = Activity
        fields = [
            'name', 'description', 'date', 'start_time', 'end_time',
            'capacity', 'location', 'organizer', 'tags', 'tag_ids',
            'category', 'image'
        ]
    
    def validate_capacity(self, value):
        if value <= 0:
            raise serializers.ValidationError("จำนวนรับต้องมากกว่า 0")
        return value
    
    def validate(self, data):
        start_time = data.get('start_time')
        end_time = data.get('end_time')
        
        if start_time and end_time and end_time <= start_time:
            raise serializers.ValidationError({
                'end_time': 'เวลาสิ้นสุดต้องมากกว่าเวลาเริ่มต้น'
            })
        
        return data
    
    def create(self, validated_data):
        # แยก tag_ids ออกก่อน
        tag_ids = validated_data.pop('tag_ids', [])
        
        if 'tags' not in validated_data or not validated_data.get('tags'):
            validated_data['tags'] = ''
        
        # สร้าง Activity
        activity = Activity.objects.create(**validated_data)
        
        # เพิ่ม Tags
        if tag_ids:
            for tag_id in tag_ids:
                try:
                    tag = Tag.objects.get(id=tag_id)
                    ActivityTag.objects.create(activity=activity, tag=tag)
                except Tag.DoesNotExist:
                    pass
        
        return activity


#แก้ไขกิจกรรม
class ActivityUpdateSerializer(serializers.ModelSerializer):
    """Serializer สำหรับแก้ไขกิจกรรม"""
    
    tags = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    
    # 🆕 รับ tag_ids สำหรับอัพเดท
    tag_ids = serializers.ListField(
        child=serializers.IntegerField(),
        required=False,
        write_only=True
    )
    
    image = serializers.ImageField(required=False, allow_null=True)
    start_time = serializers.TimeField(required=False, allow_null=True, format='%H:%M')
    end_time = serializers.TimeField(required=False, allow_null=True, format='%H:%M')
    
    class Meta:
        model = Activity
        fields = [
            'name', 'description', 'date', 'start_time', 'end_time',
            'capacity', 'location', 'organizer', 'tags', 'tag_ids',
            'category', 'image', 'status'
        ]
        extra_kwargs = {
            'name': {'required': False},
            'description': {'required': False},
            'date': {'required': False},
            'capacity': {'required': False},
            'location': {'required': False},
            'organizer': {'required': False},
            'category': {'required': False},
            'status': {'required': False},
        }
    
    def validate_capacity(self, value):
        if value and value <= 0:
            raise serializers.ValidationError("จำนวนรับต้องมากกว่า 0")
        return value
    
    def validate(self, data):
        start_time = data.get('start_time')
        end_time = data.get('end_time')
        
        if start_time and end_time and end_time <= start_time:
            raise serializers.ValidationError({
                'end_time': 'เวลาสิ้นสุดต้องมากกว่าเวลาเริ่มต้น'
            })
        
        return data
    
    def update(self, instance, validated_data):
        # แยก tag_ids ออกก่อน
        tag_ids = validated_data.pop('tag_ids', None)
        
        # อัพเดท fields อื่นๆ
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # อัพเดท Tags (ถ้ามี)
        if tag_ids is not None:
            # ลบ Tags เก่าทั้งหมด
            ActivityTag.objects.filter(activity=instance).delete()
            
            # เพิ่ม Tags ใหม่
            for tag_id in tag_ids:
                try:
                    tag = Tag.objects.get(id=tag_id)
                    ActivityTag.objects.create(activity=instance, tag=tag)
                except Tag.DoesNotExist:
                    pass
        
        return instance


#รายชื่อคนลงทะเบียนกิจกรรม
class RegistrationSerializer(serializers.ModelSerializer):
    activity = ActivitySerializer(read_only=True)
    user_name = serializers.CharField(source='user.username', read_only=True)
    user_email = serializers.CharField(source='user.email', read_only=True)
    
    class Meta:
        model = Registration
        fields = ['id', 'activity', 'user_name', 'user_email', 'phone', 'note', 'status', 'registered_at']
        read_only_fields = ['id', 'status', 'registered_at', 'activity', 'user_name', 'user_email']