from rest_framework.generics import ListAPIView, CreateAPIView, get_object_or_404
from rest_framework.views import APIView, Response

from .models import Booking, OpenMatch
from .serializers import OpenMatchListSerializer, UserBookingSerializer, CreateBookingSerializer, OpenMatchDetailSerializer
from .services import create_booking, create_open_match_player


# Create your views here.
class UserBookingListView(ListAPIView):
    serializer_class = UserBookingSerializer

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)

class OpenMatchListView(ListAPIView):
    queryset = OpenMatch.objects.filter(reservation__status='awaiting_payment')
    serializer_class = OpenMatchListSerializer

class OpenMatchDetailView(APIView):
    def get(self, request, match_id):
        try:
            match = OpenMatch.objects.get(match_id=match_id)
        except OpenMatch.DoesNotExist:
            return Response({"detail": "Open match not found"}, status=404)

        serializer = OpenMatchDetailSerializer(match)
        return Response(serializer.data)

class JoinOpenMatchView(APIView):
    def post(self, request, match_id):
        try:
            match = get_object_or_404(OpenMatch, pk=match_id)
        except OpenMatch.DoesNotExist:
            return Response({"detail": "Open match not found"}, status=404)

        participant = create_open_match_player(user=request.user, match=match)

        if participant == "FULL":
            return Response({"detail": "Match is already full"}, status=400)

        elif participant == "ALREADY_JOINED":
            return Response({"detail": "You have already joined this match"}, status=400)
        
        return Response({"detail": "Successfully joined the match"}, status=200)
    
class CreateBookingView(APIView):
    def post(self, request):
        serializer = CreateBookingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        booking = create_booking(
            user=request.user,
            data=serializer.validated_data
        )

        if booking is None:
            return Response({"detail": "Court is not available for the selected date and time"}, status=400)
        
        return Response(UserBookingSerializer(booking).data, status=201)