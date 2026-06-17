from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.views import APIView, Response

from .models import Court
from .serializers import CreateCourtSerializer, ListCourtSerializer, CourtDetailSerializer
from .services import create_court


# Create your views here.
class CourtListView(ListAPIView):
    queryset = Court.objects.all()
    serializer_class = ListCourtSerializer

class CourtCreateView(APIView):
    def post(self, request):
        serializer = CreateCourtSerializer(data=request.data)
        
        serializer.is_valid(raise_exception=True)

        court = create_court(
            owner=request.user,
            data=serializer.validated_data
        )

        return Response(ListCourtSerializer(court).data, status=201)

class CourtDetailView(APIView):
    def get(self, request, court_id):
        try:
            court = Court.objects.get(court_id=court_id)
            
        except Court.DoesNotExist:
            return Response({"detail": "Court not found"}, status=404)

        return Response(CourtDetailSerializer(court).data)