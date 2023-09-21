from rest_framework import serializers

from product_app.models import Lesson, LessonView


class LessonViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonView
        fields = ['view_time_seconds', 'status']


class LessonSerializer(serializers.ModelSerializer):
    lesson_view = LessonViewSerializer(source='views', many=True, read_only=True)

    class Meta:
        model = Lesson
        fields = ['id', 'title', 'description', 'link_video', 'durations_second', 'lesson_view']


class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    description = serializers.CharField()
    total_lessons_viewed = serializers.IntegerField()
    total_view_time = serializers.IntegerField()
    total_students = serializers.IntegerField()
    purchase_percentage = serializers.FloatField()

    class Meta:
        fields = '__all__'
