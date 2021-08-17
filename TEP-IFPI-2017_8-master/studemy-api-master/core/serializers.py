from rest_framework import serializers
from core.models import *

class DiscountCouponSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DiscountCoupon
        fields = ('discount_type', 'value', 'expiration_date', 'course')

class SmallCourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ('id', 'name')

class SubscriptionSerializer(serializers.ModelSerializer):
    course = SmallCourseSerializer(
        many=False,
        read_only=True
    )

    class Meta:
        model = Subscription
        fields = ('status', 'course','price', 'is_favorite', 'rating')

class TeacherSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True,many=False)

    class Meta:
        model = User
        fields = ('user', 'name', 'contents')

class StudentSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = User
        fields = ('id', 'name')

class UserSerializer(serializers.ModelSerializer):
    subscriptions = SubscriptionSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('id','who_is', 'name', 'username', 'subscriptions')

class CourseSerializer(serializers.HyperlinkedModelSerializer):

    user = serializers.HyperlinkedRelatedField(read_only=True,view_name='teacher_detail')

    class Meta:
        model = Course
        fields = ('id','thumb', 'name', 'created_date', 'price', 'user')
