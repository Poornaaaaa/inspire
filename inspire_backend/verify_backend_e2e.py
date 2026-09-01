import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inspire_project.settings')
django.setup()

from rest_framework.test import APIClient
from api.models import Squad, Registration, EventTrack, ScoreAuditLog

def run_e2e_verification():
    print("=" * 60)
    print("INSPIRE 2026 - DJANGO REST BACKEND E2E TEST SUITE")
    print("=" * 60)

    client = APIClient()

    # 1. Test GET /api/scores/
    print("\n[1/5] Testing GET /api/scores/...")
    res = client.get('/api/scores/')
    assert res.status_code == 200, f"Failed: {res.status_code}"
    assert res.data['status'] == 'success'
    print(f"  -> Total Squads Found: {len(res.data['data'])}")
    for sq in res.data['data'][:3]:
        print(f"     * {sq['num']}: {sq['name']} - {sq['points']} PTS")
    print("  -> GET /api/scores/ PASSED [OK]")

    # 2. Test POST /api/scores/update/
    print("\n[2/5] Testing POST /api/scores/update/ (Points Allocation)...")
    update_res = client.post('/api/scores/update/', {
        "id": "team_01",
        "delta": 100,
        "event": "IT Quiz (1st Place)"
    }, format='json')
    assert update_res.status_code == 200, f"Failed: {update_res.status_code}"
    team01 = Squad.objects.get(squad_id="team_01")
    assert team01.points >= 100, f"Points mismatch: {team01.points}"
    print(f"  -> Successfully awarded +100 PTS to {team01.name} (Current: {team01.points} PTS)")
    print("  -> POST /api/scores/update/ PASSED [OK]")

    # 3. Test POST /api/register/
    print("\n[3/5] Testing POST /api/register/ (Student Delegate Registration)...")
    import random
    test_pass_id = f"INS-2026-{random.randint(1000, 9999)}"
    reg_payload = {
        "event": "Coding and Debugging",
        "squad": "SYNDICATE",
        "teamName": "SYNDICATE · Binary Duo",
        "participants": "Pavan S, Asim Khan",
        "phone": "+91 98765 43210",
        "email": "pavan@claretcollege.edu.in",
        "year": "Year III",
        "course": "BCA",
        "section": "Section B",
        "rollNo": "23BCA102",
        "passId": test_pass_id
    }
    reg_res = client.post('/api/register/', reg_payload, format='json')
    assert reg_res.status_code == 201, f"Failed: {reg_res.status_code} - {reg_res.data}"
    assert reg_res.data['pass_id'] == test_pass_id
    print(f"  -> Registered Pass ID: {reg_res.data['pass_id']} for Event: {reg_payload['event']}")
    print("  -> POST /api/register/ PASSED [OK]")

    # 4. Test GET /api/registrations/
    print("\n[4/5] Testing GET /api/registrations/ (List & Search Filter)...")
    list_res = client.get('/api/registrations/?search=23BCA102')
    assert list_res.status_code == 200
    assert list_res.data['total_registrations'] >= 1
    print(f"  -> Search match found: {list_res.data['data'][0]['participants']} ({list_res.data['data'][0]['roll_no']})")
    print("  -> GET /api/registrations/ PASSED [OK]")

    # 5. Test POST /api/scores/reset/
    print("\n[5/5] Testing POST /api/scores/reset/ (Reset to 0 PTS)...")
    reset_res = client.post('/api/scores/reset/')
    assert reset_res.status_code == 200
    for sq in Squad.objects.all():
        assert sq.points == 0, f"Squad {sq.name} has non-zero points: {sq.points}"
    print(f"  -> All {Squad.objects.count()} squads successfully reset to 0 PTS baseline")
    print("  -> POST /api/scores/reset/ PASSED [OK]")

    print("\n" + "=" * 60)
    print("ALL 5 E2E INTEGRATION TESTS PASSED PERFECTLY (100% SUCCESS)")
    print("=" * 60)

if __name__ == '__main__':
    run_e2e_verification()
