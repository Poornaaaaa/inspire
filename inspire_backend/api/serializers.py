import random
from rest_framework import serializers
from .models import Squad, Registration, EventTrack, ScoreAuditLog

class SquadSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='squad_id', read_only=True)

    class Meta:
        model = Squad
        fields = ['id', 'squad_id', 'num', 'name', 'captain', 'vice_captain', 'points', 'badge_color', 'updated_at']


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registration
        fields = [
            'id', 'pass_id', 'event_name', 'squad_name', 'team_name',
            'participants', 'phone', 'email', 'year', 'course',
            'section', 'roll_no', 'venue', 'time', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']

    def create(self, validated_data):
        if not validated_data.get('pass_id'):
            validated_data['pass_id'] = f"INS-2026-{random.randint(1000, 9999)}"
        return super().create(validated_data)


class EventTrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventTrack
        fields = '__all__'


class ScoreAuditLogSerializer(serializers.ModelSerializer):
    squad_name = serializers.CharField(source='squad.name', read_only=True)

    class Meta:
        model = ScoreAuditLog
        fields = ['id', 'squad_name', 'delta_points', 'resulting_points', 'event_name', 'allocated_by', 'notes', 'timestamp']
