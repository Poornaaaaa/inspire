import os
import hashlib
import hmac
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.db.models import Q
from .models import Squad, Registration, EventTrack, ScoreAuditLog
from .serializers import SquadSerializer, RegistrationSerializer, EventTrackSerializer, ScoreAuditLogSerializer

class LeaderboardAPIView(APIView):
    """
    GET /api/scores/
    Returns live score standings for all 11 squads.
    """
    permission_classes = [AllowAny]

    def get(self, request):
        squads = Squad.objects.all().order_by('-points', 'squad_id')
        serializer = SquadSerializer(squads, many=True)
        return Response({
            "status": "success",
            "count": squads.count(),
            "data": serializer.data
        }, status=status.HTTP_200_OK)


class UpdateScoresAPIView(APIView):
    """
    POST /api/scores/update/
    Updates points for one or multiple squads from the Admin scoring console.
    Accepts:
      - Batch array: [{"id": "team_01", "points": 120}, ...]
      - Single squad object: {"id": "team_01", "points": 120, "event": "IT Quiz"}
      - Delta adjustment: {"id": "team_01", "delta": 50, "event": "Coding"}
    """
    permission_classes = [AllowAny]

    def post(self, request):
        payload = request.data

        # Handle batch array of squad updates
        if isinstance(payload, list):
            updated_squads = []
            for item in payload:
                squad_key = item.get('id') or item.get('squad_id') or item.get('num')
                pts = item.get('points')
                if squad_key is not None and pts is not None:
                    squad = Squad.objects.filter(
                        Q(squad_id__iexact=squad_key) | 
                        Q(num__iexact=squad_key) | 
                        Q(name__iexact=squad_key)
                    ).first()
                    if squad:
                        old_pts = squad.points
                        squad.points = int(pts)
                        squad.save()
                        ScoreAuditLog.objects.create(
                            squad=squad,
                            delta_points=squad.points - old_pts,
                            resulting_points=squad.points,
                            event_name=item.get('event', 'Batch Score Sync'),
                            allocated_by="admin"
                        )
                        updated_squads.append(squad)

            squads = Squad.objects.all().order_by('-points', 'squad_id')
            return Response({
                "status": "success",
                "message": f"Successfully updated {len(updated_squads)} squad scores",
                "data": SquadSerializer(squads, many=True).data
            }, status=status.HTTP_200_OK)

        # Handle single squad update
        elif isinstance(payload, dict):
            squad_key = payload.get('id') or payload.get('squad_id') or payload.get('name') or payload.get('num')
            squad = Squad.objects.filter(
                Q(squad_id__iexact=squad_key) | 
                Q(num__iexact=squad_key) | 
                Q(name__iexact=squad_key)
            ).first()

            if not squad:
                return Response({
                    "status": "error",
                    "message": f"Squad '{squad_key}' not found"
                }, status=status.HTTP_404_NOT_FOUND)

            old_pts = squad.points
            if 'delta' in payload:
                delta = int(payload['delta'])
                squad.points += delta
            elif 'points' in payload:
                squad.points = int(payload['points'])
                delta = squad.points - old_pts
            else:
                delta = 0

            squad.save()

            ScoreAuditLog.objects.create(
                squad=squad,
                delta_points=delta,
                resulting_points=squad.points,
                event_name=payload.get('event', payload.get('eventName', 'Manual Points Allocation')),
                allocated_by=payload.get('allocatedBy', 'admin'),
                notes=payload.get('notes', '')
            )

            squads = Squad.objects.all().order_by('-points', 'squad_id')
            return Response({
                "status": "success",
                "message": f"Updated {squad.name} score to {squad.points} PTS",
                "squad": SquadSerializer(squad).data,
                "data": SquadSerializer(squads, many=True).data
            }, status=status.HTTP_200_OK)

        return Response({
            "status": "error",
            "message": "Invalid payload format. Expected JSON object or array."
        }, status=status.HTTP_400_BAD_REQUEST)


class ResetScoresAPIView(APIView):
    """
    POST /api/scores/reset/
    Resets all 11 squad scores to 0.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        Squad.objects.all().update(points=0)
        squads = Squad.objects.all().order_by('squad_id')
        return Response({
            "status": "success",
            "message": "All 11 squad scores have been reset to 0 PTS",
            "data": SquadSerializer(squads, many=True).data
        }, status=status.HTTP_200_OK)


class RegistrationCreateAPIView(APIView):
    """
    POST /api/register/
    Receives delegate registration payload from index.html and logs to database.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data

        # Normalize field names from frontend camelCase/standard
        payload = {
            'pass_id': data.get('passId') or data.get('pass_id'),
            'event_name': data.get('event') or data.get('eventName') or data.get('event_name', 'General Entry'),
            'squad_name': data.get('squad') or data.get('squadName') or data.get('squad_name', 'Unassigned'),
            'team_name': data.get('teamName') or data.get('team_name', ''),
            'participants': data.get('participants') or data.get('participantNames', 'Participant'),
            'phone': data.get('phone', ''),
            'email': data.get('email', ''),
            'year': data.get('year', ''),
            'course': data.get('course', 'BCA'),
            'section': data.get('section', ''),
            'roll_no': (data.get('rollNo') or data.get('roll_no', '')).upper().strip(),
            'venue': data.get('venue', 'St. Claret College Campus'),
            'time': data.get('time', 'Event Day (Sept 10, 2026)')
        }

        serializer = RegistrationSerializer(data=payload)
        if serializer.is_valid():
            reg = serializer.save()
            return Response({
                "status": "success",
                "message": "Delegate registration confirmed and recorded successfully",
                "pass_id": reg.pass_id,
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response({
            "status": "error",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class RegistrationListAPIView(APIView):
    """
    GET /api/registrations/
    Lists all registered student delegates with optional filtering by event, squad, or search keyword.
    """
    permission_classes = [AllowAny]

    def get(self, request):
        qs = Registration.objects.all().order_by('-created_at')

        event_filter = request.query_params.get('event')
        squad_filter = request.query_params.get('squad')
        search = request.query_params.get('search')

        if event_filter:
            qs = qs.filter(event_name__icontains=event_filter)
        if squad_filter:
            qs = qs.filter(squad_name__icontains=squad_filter)
        if search:
            qs = qs.filter(
                Q(participants__icontains=search) |
                Q(roll_no__icontains=search) |
                Q(phone__icontains=search) |
                Q(pass_id__icontains=search)
            )

        serializer = RegistrationSerializer(qs, many=True)
        return Response({
            "status": "success",
            "total_registrations": qs.count(),
            "data": serializer.data
        }, status=status.HTTP_200_OK)


class AdminLoginAPIView(APIView):
    """
    POST /api/admin/login/
    Validates administrator login credentials using secure SHA-256 cryptographic hashing.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        admin_id = request.data.get('id', '').strip()
        admin_pass = request.data.get('password', '').strip()

        if not admin_id or not admin_pass:
            return Response({
                "status": "error",
                "authenticated": False,
                "message": "Admin ID and Password are required."
            }, status=status.HTTP_400_BAD_REQUEST)

        # Expected credentials from environment or encrypted default
        expected_id = os.environ.get("ADMIN_ID", "admin")

        if "ADMIN_PASSWORD" in os.environ:
            expected_hash = hashlib.sha256(os.environ["ADMIN_PASSWORD"].encode('utf-8')).hexdigest()
        else:
            expected_hash = os.environ.get(
                "ADMIN_PASSWORD_HASH",
                "3c9bce422677b7891051127ddb31392481f22dedd2b75aa4cbf45669f0f3744b"
            )

        # Compute SHA-256 hash of provided password
        provided_hash = hashlib.sha256(admin_pass.encode('utf-8')).hexdigest()

        # Constant-time comparison to prevent timing attacks
        id_valid = hmac.compare_digest(admin_id, expected_id)
        pass_valid = hmac.compare_digest(provided_hash, expected_hash)

        if id_valid and pass_valid:
            return Response({
                "status": "success",
                "authenticated": True,
                "message": "Admin authorization granted",
                "role": "Chief Fest Coordinator"
            }, status=status.HTTP_200_OK)

        return Response({
            "status": "error",
            "authenticated": False,
            "message": "Invalid Admin Credentials. Access Denied."
        }, status=status.HTTP_401_UNAUTHORIZED)


class EventListAPIView(APIView):
    """
    GET /api/events/
    Returns the 14 competition tracks.
    """
    permission_classes = [AllowAny]

    def get(self, request):
        events = EventTrack.objects.all()
        return Response({
            "status": "success",
            "count": events.count(),
            "data": EventTrackSerializer(events, many=True).data
        }, status=status.HTTP_200_OK)
