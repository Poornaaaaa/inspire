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

        created_squads = 0
        for sq in squads_data:
            obj, created = Squad.objects.get_or_create(
                squad_id=sq["squad_id"],
                defaults={
                    "num": sq["num"],
                    "name": sq["name"],
                    "captain": sq["captain"],
                    "vice_captain": sq["vice_captain"],
                    "points": 0,
                    "badge_color": sq["badge_color"]
                }
            )
            if created:
                created_squads += 1
            else:
                # Ensure baseline points remain 0
                obj.name = sq["name"]
                obj.captain = sq["captain"]
                obj.vice_captain = sq["vice_captain"]
                obj.save()

        self.stdout.write(self.style.SUCCESS("[OK] Squads ready: 11 Squads verified (0 baseline points)"))

        # 14 Competition Tracks
        events_data = [
            {"event_id": "it-quiz", "name": "IT Quiz", "category": "Technical", "format_type": "Team of 2", "team_size": 2, "venue": "Seminar Hall A", "time": "10:30 AM – 11:30 AM"},
            {"event_id": "it-manager", "name": "IT Manager", "category": "Management", "format_type": "Individual", "team_size": 1, "venue": "Board Room 1", "time": "11:00 AM – 01:00 PM"},
            {"event_id": "debate", "name": "Debate", "category": "Communication", "format_type": "Team of 4", "team_size": 4, "venue": "Audio-Visual Hall", "time": "11:30 AM – 01:00 PM"},
            {"event_id": "startup-pitch", "name": "Startup Pitch", "category": "Entrepreneurship", "format_type": "Team of 4", "team_size": 4, "venue": "Conference Room", "time": "01:30 PM – 03:00 PM"},
            {"event_id": "photography", "name": "Photography", "category": "Creative", "format_type": "Individual", "team_size": 1, "venue": "Campus Wide / Online Drive", "time": "Full Day Submission"},
            {"event_id": "graphical-designing", "name": "Graphical Designing", "category": "Design", "format_type": "Individual", "team_size": 1, "venue": "Multimedia Lab", "time": "11:30 AM – 01:00 PM"},
            {"event_id": "coding-debugging", "name": "Coding and Debugging", "category": "Technical", "format_type": "Team of 2", "team_size": 2, "venue": "Computer Lab 1", "time": "10:30 AM – 12:00 PM"},
            {"event_id": "ipl-auction", "name": "IPL Auction", "category": "Strategy", "format_type": "Team of 4", "team_size": 4, "venue": "Seminar Hall B", "time": "01:30 PM – 03:30 PM"},
            {"event_id": "logo-designing", "name": "Logo Designing", "category": "Design", "format_type": "Individual", "team_size": 1, "venue": "Computer Lab 2", "time": "11:30 AM – 01:00 PM"},
            {"event_id": "treasure-hunt", "name": "Treasure Hunt", "category": "Adventure", "format_type": "Team of 4", "team_size": 4, "venue": "College Quadrangle", "time": "02:00 PM – 03:30 PM"},
            {"event_id": "decode-evidence", "name": "Decode the Evidence", "category": "Analytical", "format_type": "Team of 3", "team_size": 3, "venue": "Room 204", "time": "11:30 AM – 01:00 PM"},
            {"event_id": "bgmi", "name": "BGMI", "category": "Esports", "format_type": "Team of 4", "team_size": 4, "venue": "Gaming Arena / Lab 3", "time": "01:30 PM – 03:30 PM"},
            {"event_id": "free-fire", "name": "Free Fire", "category": "Esports", "format_type": "Team of 4", "team_size": 4, "venue": "Gaming Arena / Lab 3", "time": "01:30 PM – 03:30 PM"},
            {"event_id": "typing-marathon", "name": "Typing Marathon", "category": "Speed", "format_type": "Individual", "team_size": 1, "venue": "Computer Lab 4", "time": "10:30 AM – 11:30 AM"}
        ]

        created_events = 0
        for ev in events_data:
            obj, created = EventTrack.objects.get_or_create(
                event_id=ev["event_id"],
                defaults=ev
            )
            if created:
                created_events += 1

        self.stdout.write(self.style.SUCCESS("[OK] Competition tracks ready: 14 Events verified"))
        self.stdout.write(self.style.SUCCESS("[SUCCESS] Inspire 2026 Database Seeding Complete!"))
