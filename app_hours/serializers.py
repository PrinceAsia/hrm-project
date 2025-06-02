from datetime import time, datetime
from django.utils.timezone import now
from rest_framework import serializers

from .models import WorkPlaces, WorkingHours


class WorkPlacesSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkPlaces
        fields = '__all__'


class WorkingHoursSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkingHours
        fields = '__all__'
        read_only_fields = ('user',)

    def validate_work_day(self, value):
        today = now().date()
        current_time = now().time()

        if value > today:
            raise serializers.ValidationError("Kelajakdagi sanalar uchun ish vaqtini kiritish mumkin emas.")
        if value == today and current_time < time(18, 0):
            raise serializers.ValidationError("Bugungi ish vaqtini faqat 18:00 dan keyin kiritish mumkin.")
        return value

    def validate(self, data):
        user = self.context['request'].user
        if WorkingHours.objects.filter(work_day=data['work_day'], user=user).exists():
            raise serializers.ValidationError("Siz ushbu kunga ish vaqtini allaqachon kiritgansiz.")
        return data

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)