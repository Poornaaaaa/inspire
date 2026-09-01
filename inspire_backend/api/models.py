from django.db import models

class Squad(models.Model):
    """
    Represents one of the 11 official competing squads in Inspire 2026.
    Points default to 0 and update dynamically during live events.
    """
    squad_id = models.CharField(max_length=50, unique=True, help_text="e.g. team_01")
    num = models.CharField(max_length=50, help_text="e.g. Team 01")
    name = models.CharField(max_length=150, unique=True, help_text="e.g. TEAM CHRONIX")
    captain = models.CharField(max_length=150, blank=True)
    vice_captain = models.CharField(max_length=150, blank=True)
    points = models.IntegerField(default=0, help_text="Total accumulated points")
    badge_color = models.CharField(max_length=50, default="#10B981")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-points', 'squad_id']
        verbose_name = 'Squad Score'
        verbose_name_plural = 'Squad Scores (11 Teams)'

    def __str__(self):
        return f"{self.num} · {self.name} ({self.points} PTS)"


class Registration(models.Model):
    """
    Student delegate registration entries from index.html registration form.
    """
    pass_id = models.CharField(max_length=50, unique=True, help_text="e.g. INS-2026-8491")
    event_name = models.CharField(max_length=150)
    squad_name = models.CharField(max_length=150)
    team_name = models.CharField(max_length=200, blank=True, null=True)
    participants = models.TextField(help_text="Comma-separated participant delegate names")
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    year = models.CharField(max_length=50)
    course = models.CharField(max_length=100, default="BCA")
    section = models.CharField(max_length=50)
    roll_no = models.CharField(max_length=50)
    venue = models.CharField(max_length=150, blank=True, null=True)
    time = models.CharField(max_length=150, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Delegate Registration'
        verbose_name_plural = 'Delegate Registrations'

    def __str__(self):
        return f"[{self.pass_id}] {self.roll_no} - {self.event_name} ({self.squad_name})"


class EventTrack(models.Model):
    """
    14 official competition tracks for Inspire 2026.
    """
    event_id = models.CharField(max_length=100, unique=True, help_text="e.g. it-quiz")
    name = models.CharField(max_length=150)
    category = models.CharField(max_length=100)
    format_type = models.CharField(max_length=50, help_text="Individual or Team")
    team_size = models.IntegerField(default=1)
    venue = models.CharField(max_length=150)
    time = models.CharField(max_length=150)

    class Meta:
        ordering = ['id']
        verbose_name = 'Competition Track'
        verbose_name_plural = 'Competition Tracks (14 Events)'

    def __str__(self):
        return f"{self.name} ({self.format_type})"


class ScoreAuditLog(models.Model):
    """
    Audit log of all score allocations made by admin in admin.html.
    """
    squad = models.ForeignKey(Squad, on_delete=models.CASCADE, related_name='score_logs')
    delta_points = models.IntegerField(help_text="Points added or subtracted")
    resulting_points = models.IntegerField(help_text="Score after modification")
    event_name = models.CharField(max_length=150, blank=True, null=True)
    allocated_by = models.CharField(max_length=100, default="admin")
    notes = models.CharField(max_length=255, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Score Audit Log'
        verbose_name_plural = 'Score Audit Logs'

    def __str__(self):
        sign = "+" if self.delta_points >= 0 else ""
        return f"{self.squad.name}: {sign}{self.delta_points} PTS -> {self.resulting_points} PTS ({self.timestamp:%d/%m %H:%M})"
