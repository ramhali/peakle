from rest_framework import serializers

from .models import Booking, OpenMatch, MatchParticipant

class UserBookingSerializer(serializers.ModelSerializer): # for both creation and listing of bookings
    class Meta:
        model = Booking
        fields = [
            "court",
            "status",
            "date",
            "start_time",
            "end_time"
        ]


class CreateOpenMatchBookingSerializer(serializers.Serializer):
    skill_level = serializers.ChoiceField(choices=OpenMatch.SKILL_LEVELS)
    type = serializers.ChoiceField(choices=OpenMatch.MATCH_TYPES)
    max_players = serializers.IntegerField(min_value=1)
    description = serializers.CharField(required=False, allow_blank=True)

class CreateBookingSerializer(serializers.ModelSerializer):
    open_match_data = CreateOpenMatchBookingSerializer(required=False, allow_null=True)

    class Meta:
        model = Booking
        fields = [
            "court",
            "date",
            "start_time",
            "end_time",
            "is_open_match",
            "open_match_data"
        ]

class OpenMatchListSerializer(serializers.ModelSerializer):
    reservation_details = serializers.SerializerMethodField()
    
    class Meta:
        model = OpenMatch
        fields = [
            "skill_level",
            "type",
            "max_players",
            "description",
            "reservation_details"
        ]
    
    def get_reservation_details(self, obj):
        reservation = obj.reservation
        return {
            "court": reservation.court.court_name,
            "date": reservation.date,
            "start_time": reservation.start_time,
            "end_time": reservation.end_time,
        }

class MatchParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = MatchParticipant
        fields = [
            "user",
            "status",
            "joined_at"
        ]

class OpenMatchDetailSerializer(OpenMatchListSerializer):
    participants = MatchParticipantSerializer(many=True, read_only=True)
    
    class Meta(OpenMatchListSerializer.Meta):
        fields = OpenMatchListSerializer.Meta.fields + ["participants"]