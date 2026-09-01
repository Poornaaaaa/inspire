from django.test import TestCase
from rest_framework.test import APIClient
from api.models import Squad, Registration, EventTrack

class InspireAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.squad1 = Squad.objects.create(
            squad_id="team_01",
            num="Team 01",
            name="TEAM CHRONIX",
            captain="Veronica Vinutha K",
            points=0
        )
        self.squad2 = Squad.objects.create(
            squad_id="team_02",
            num="Team 02",
            name="SYNDICATE",
            captain="Pavan S",
            points=0
        )

    def test_get_scores(self):
        response = self.client.get('/api/scores/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['status'], 'success')
        self.assertEqual(len(response.data['data']), 2)
        self.assertEqual(response.data['data'][0]['points'], 0)

    def test_update_scores_single_and_batch(self):
        # Test single delta allocation
        res1 = self.client.post('/api/scores/update/', {
            "id": "team_01",
            "delta": 100,
            "event": "IT Quiz"
        }, format='json')
        self.assertEqual(res1.status_code, 200)
        self.squad1.refresh_from_db()
        self.assertEqual(self.squad1.points, 100)

        # Test batch allocation
        res2 = self.client.post('/api/scores/update/', [
            {"id": "team_01", "points": 150},
            {"id": "team_02", "points": 90}
        ], format='json')
        self.assertEqual(res2.status_code, 200)
        self.squad1.refresh_from_db()
        self.squad2.refresh_from_db()
        self.assertEqual(self.squad1.points, 150)
        self.assertEqual(self.squad2.points, 90)

    def test_registration_create_and_list(self):
        reg_payload = {
            "event": "IT Quiz",
            "squad": "TEAM CHRONIX",
            "teamName": "TEAM CHRONIX · Duo Alpha",
            "participants": "Veronica, Sunidhi",
            "phone": "9876543210",
            "email": "test@claretcollege.edu.in",
            "year": "Year II",
            "course": "BCA",
            "section": "Section A",
            "rollNo": "24BCA001",
            "passId": "INS-2026-9999"
        }
        res = self.client.post('/api/register/', reg_payload, format='json')
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.data['pass_id'], 'INS-2026-9999')

        # List registrations
        list_res = self.client.get('/api/registrations/')
        self.assertEqual(list_res.status_code, 200)
        self.assertEqual(list_res.data['total_registrations'], 1)
        self.assertEqual(list_res.data['data'][0]['roll_no'], '24BCA001')

    def test_reset_scores(self):
        self.squad1.points = 100
        self.squad1.save()
        res = self.client.post('/api/scores/reset/')
        self.assertEqual(res.status_code, 200)
        self.squad1.refresh_from_db()
        self.assertEqual(self.squad1.points, 0)
