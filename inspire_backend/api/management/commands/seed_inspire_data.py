from django.core.management.base import BaseCommand
from api.models import Squad, EventTrack

class Command(BaseCommand):
    help = 'Seeds initial 11 Squads (with 0 PTS) and 14 Competition Tracks for Inspire 2026'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Seeding Inspire 2026 squads and competitions..."))

        # 11 Official Competing Squads (All start at 0 PTS)
        squads_data = [
            {"squad_id": "team_01", "num": "Team 01", "name": "TEAM CHRONIX", "captain": "Veronica Vinutha K", "vice_captain": "Sunidhi Chandra", "badge_color": "#10B981"},
            {"squad_id": "team_02", "num": "Team 02", "name": "SYNDICATE", "captain": "Pavan S", "vice_captain": "Asim Khan", "badge_color": "#06B6D4"},
            {"squad_id": "team_03", "num": "Team 03", "name": "QUANTUM PARADOX", "captain": "Yuvaraj S", "vice_captain": "Prerana S", "badge_color": "#6366F1"},
            {"squad_id": "team_04", "num": "Team 04", "name": "VERA", "captain": "Madhura H K", "vice_captain": "Himani P", "badge_color": "#EC4899"},
            {"squad_id": "team_05", "num": "Team 05", "name": "ERA-X", "captain": "Eshwari P", "vice_captain": "Sinchana V", "badge_color": "#F59E0B"},
            {"squad_id": "team_06", "num": "Team 06", "name": "ERONX", "captain": "Zoya Fathima", "vice_captain": "Simran Bharatiya", "badge_color": "#8B5CF6"},
            {"squad_id": "team_07", "num": "Team 07", "name": "TIME LOOP", "captain": "Harshitha R", "vice_captain": "Adhithi Rashmi D", "badge_color": "#14B8A6"},
            {"squad_id": "team_08", "num": "Team 08", "name": "PRABHUTVA", "captain": "Hamsa Lakshmi G", "vice_captain": "Prerana S", "badge_color": "#EF4444"},
            {"squad_id": "team_09", "num": "Team 09", "name": "YUGANTARA", "captain": "Yashaswini C", "vice_captain": "Haripriya O", "badge_color": "#3B82F6"},
            {"squad_id": "team_10", "num": "Team 10", "name": "EVARA", "captain": "Sanjana S Shetty", "vice_captain": "Chinmayi S H", "badge_color": "#10B981"},
            {"squad_id": "team_11", "num": "Team 11", "name": "CHRONO CREW", "captain": "Rishika D", "vice_captain": "Manya R", "badge_color": "#F97316"}
        ]

        for sq in squads_data:
            Squad.objects.update_or_create(
                squad_id=sq["squad_id"],
                defaults={
                    "num": sq["num"],
                    "name": sq["name"],
                    "captain": sq["captain"],
                    "vice_captain": sq["vice_captain"],
                    "badge_color": sq["badge_color"]
                }
            )

        self.stdout.write(self.style.SUCCESS("[OK] Squads ready: 11 Squads verified"))

        # 14 Official Competition Tracks
        events_data = [
            {"event_id": "it-quiz", "name": "IT Quiz", "category": "Technical", "format_type": "Team of 2", "team_size": 2, "venue": "Mother Teresa Conference Hall – Admin Block", "time": "10:30 AM – 11:15 AM"},
            {"event_id": "it-manager", "name": "IT Manager", "category": "Corporate", "format_type": "Individual", "team_size": 1, "venue": "APJ Abdul Kalam Auditorium – Admin Block", "time": "10:30 AM – 02:00 PM"},
            {"event_id": "coding-debugging", "name": "Coding and Debugging", "category": "Technical", "format_type": "Team of 2", "team_size": 2, "venue": "III Floor LAB – Annex Block", "time": "11:00 AM – 12:15 PM"},
            {"event_id": "decode-evidence", "name": "Decode the Evidence", "category": "Technical", "format_type": "Team of 3", "team_size": 3, "venue": "Room No 117 – Annex Block", "time": "11:15 AM – 12:15 PM"},
            {"event_id": "startup-pitch", "name": "Startup Pitch", "category": "Corporate", "format_type": "Team of 4", "team_size": 4, "venue": "Room No 218 – Annex Block", "time": "01:15 PM – 02:30 PM"},
            {"event_id": "treasure-hunt", "name": "Treasure Hunt", "category": "General", "format_type": "Team of 4", "team_size": 4, "venue": "Room No 116 – Annex Block", "time": "12:50 PM – 01:50 PM"},
            {"event_id": "photography", "name": "Photography", "category": "Creative", "format_type": "Individual", "team_size": 1, "venue": "Information will be given through WhatsApp group", "time": "Information will be given through WhatsApp group"},
            {"event_id": "logo-designing", "name": "Logo Designing", "category": "Creative", "format_type": "Individual", "team_size": 1, "venue": "Information will be given through WhatsApp group", "time": "Information will be given through WhatsApp group"},
            {"event_id": "graphical-designing", "name": "Graphical Designing", "category": "Creative", "format_type": "Individual", "team_size": 1, "venue": "Information will be given through WhatsApp group", "time": "Information will be given through WhatsApp group"},
            {"event_id": "ipl-auction", "name": "IPL Auction", "category": "General", "format_type": "Team of 4", "team_size": 4, "venue": "Seminar Hall – Annex Block", "time": "10:30 AM – 11:15 AM"},
            {"event_id": "typing-marathon", "name": "Typing Marathon", "category": "Technical", "format_type": "Individual", "team_size": 1, "venue": "II Floor Lab – Annex Block", "time": "11:15 AM – 12:15 PM"},
            {"event_id": "free-fire", "name": "Free Fire", "category": "Gaming", "format_type": "Team of 4", "team_size": 4, "venue": "Room No 216 – Annex Block", "time": "12:45 PM – 02:00 PM"},
            {"event_id": "bgmi", "name": "BGMI", "category": "Gaming", "format_type": "Team of 4", "team_size": 4, "venue": "Room No 217 – Annex Block", "time": "10:30 AM – 12:00 PM"},
            {"event_id": "debate", "name": "Debate", "category": "Corporate", "format_type": "Team of 4", "team_size": 4, "venue": "Seminar Hall – Annex Block", "time": "01:00 PM – 02:25 PM"}
        ]

        # Clean old tracks if needed
        EventTrack.objects.exclude(event_id__in=[e["event_id"] for e in events_data]).delete()

        for ev in events_data:
            EventTrack.objects.update_or_create(
                event_id=ev["event_id"],
                defaults=ev
            )

        self.stdout.write(self.style.SUCCESS("[OK] Competition tracks ready: 14 Events verified with official venues & timings"))
        self.stdout.write(self.style.SUCCESS("[SUCCESS] Inspire 2026 Database Seeding Complete!"))
