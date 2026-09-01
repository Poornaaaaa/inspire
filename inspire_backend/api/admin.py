from django.contrib import admin
from .models import Squad, Registration, EventTrack, ScoreAuditLog

@admin.register(Squad)
class SquadAdmin(admin.ModelAdmin):
    list_display = ('squad_id', 'num', 'name', 'captain', 'vice_captain', 'points', 'updated_at')
    list_editable = ('points',)
    search_fields = ('name', 'captain', 'vice_captain')
    ordering = ('-points', 'squad_id')


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('pass_id', 'roll_no', 'event_name', 'squad_name', 'participants', 'phone', 'year', 'section', 'created_at')
    list_filter = ('event_name', 'squad_name', 'year', 'section')
    search_fields = ('pass_id', 'roll_no', 'participants', 'phone', 'email')
    date_hierarchy = 'created_at'


@admin.register(EventTrack)
class EventTrackAdmin(admin.ModelAdmin):
    list_display = ('event_id', 'name', 'category', 'format_type', 'team_size', 'venue', 'time')
    list_filter = ('category', 'format_type')
    search_fields = ('name', 'venue')


@admin.register(ScoreAuditLog)
class ScoreAuditLogAdmin(admin.ModelAdmin):
    list_display = ('squad', 'delta_points', 'resulting_points', 'event_name', 'allocated_by', 'timestamp')
    list_filter = ('squad', 'allocated_by', 'event_name')
    date_hierarchy = 'timestamp'
