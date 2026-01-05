# backend/users/serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    profile = serializers.DictField(write_only=True, required=False)

    class Meta:
        model = User
        # ⭐ เพิ่ม last_name เข้าไป
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'profile']

    def create(self, validated_data):
        profile_data = validated_data.pop('profile', {})
        
        # ⭐ เพิ่ม last_name ในการสร้าง User
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '') # บันทึกนามสกุล
        )
        
        # อัปเดต Profile (ที่ถูกสร้างจาก Signal)
        if profile_data:
            profile = user.profile
            for key, value in profile_data.items():
                if hasattr(profile, key):
                    setattr(profile, key, value)
            profile.save()
            
        return user

# ... (ส่วนอื่นของไฟล์คงเดิม)
class UserProfileSerializer(serializers.ModelSerializer):
    profile_image = serializers.SerializerMethodField()
    class Meta:
        model = UserProfile
        fields = ['id', 'profile_image', 'phone', 'bio', 'organizer_status', 'gender', 'faculty', 'birthdate']
    
    def get_profile_image(self, obj):
        if obj.profile_image:
            request = self.context.get('request')
            if request is not None:
                return request.build_absolute_uri(obj.profile_image.url)
            return obj.profile_image.url
        return None

class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)
    fullname = serializers.SerializerMethodField()
    date_joined = serializers.DateTimeField(format='%d %B %Y', read_only=True)
    organizer_status = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'fullname', 'is_superuser', 'is_staff', 'date_joined', 'profile', 'organizer_status']
        read_only_fields = ['id', 'username', 'is_superuser', 'is_staff', 'date_joined']
    
    def get_fullname(self, obj):
        if obj.first_name and obj.last_name:
            return f"{obj.first_name} {obj.last_name}"
        elif obj.first_name:
            return obj.first_name
        return obj.username

    def get_organizer_status(self, obj):
        try:
            return obj.profile.organizer_status
        except:
            return 'none'

class UserUpdateSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(write_only=True, required=False, allow_blank=True)
    bio = serializers.CharField(write_only=True, required=False, allow_blank=True)
    gender = serializers.CharField(write_only=True, required=False, allow_blank=True)
    faculty = serializers.CharField(write_only=True, required=False, allow_blank=True)
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'bio', 'gender', 'faculty']
    
    def update(self, instance, validated_data):
        phone = validated_data.pop('phone', None)
        bio = validated_data.pop('bio', None)
        gender = validated_data.pop('gender', None)
        faculty = validated_data.pop('faculty', None)
        
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.save()
        
        try:
            profile = instance.profile
        except UserProfile.DoesNotExist:
            profile = UserProfile.objects.create(user=instance)
        
        if phone is not None: profile.phone = phone
        if bio is not None: profile.bio = bio
        if gender is not None: profile.gender = gender
        if faculty is not None: profile.faculty = faculty
        profile.save()
        
        return instance