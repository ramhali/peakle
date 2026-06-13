from rest_framework import serializers

from courts.models import Court, CourtSchedule

class CreateCourtScheduleSerializer(serializers.Serializer):
    day_of_week = serializers.ChoiceField(choices=CourtSchedule.DayOfWeek.choices)
    opening_time = serializers.TimeField()
    closing_time = serializers.TimeField()

class ListCourtScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourtSchedule
        fields = ["day_of_week", "opening_time", "closing_time"]
        
class CreateCourtSerializer(serializers.ModelSerializer):
    court_schedules = CreateCourtScheduleSerializer(many=True, required=False)
    court_images = serializers.ListField(child=serializers.ImageField(), required=False)
    court_amenities = serializers.ListField(child=serializers.CharField(), required=False)

    class Meta:
        model = Court
        fields = [
            "court_name",
            "court_type",
            "location",
            "rate",
            "description",
            "court_schedules",
            "court_images",
            "court_amenities",
        ]

class ListCourtSerializer(serializers.ModelSerializer):
    court_schedules = serializers.SerializerMethodField()
    court_images = serializers.SerializerMethodField()
    court_amenities = serializers.SerializerMethodField()

    class Meta:
        model = Court
        fields = [
            "court_name",
            "court_type",
            "location",
            "rate",
            "description",
            "court_schedules",
            "court_images",
            "court_amenities",
        ]

    def get_court_images(self, obj):
        return [img.image.url for img in obj.images.all()]

    def get_court_amenities(self, obj):
        return [a.amenity_name for a in obj.amenities.all()]

    def get_court_schedules(self, obj):
        return ListCourtScheduleSerializer(obj.schedules.all(), many=True).data

class CourtDetailSerializer(ListCourtSerializer):
    court_schedules = serializers.SerializerMethodField()
    court_reviews = serializers.SerializerMethodField()

    class Meta(ListCourtSerializer.Meta):
        fields = ListCourtSerializer.Meta.fields + [
            "court_schedules",
            "court_reviews",
        ]

    def get_court_schedules(self, obj):
        return [
            {
                "day_of_week": s.day_of_week,
                "opening_time": s.opening_time,
                "closing_time": s.closing_time,
            }
            for s in obj.schedules.all()
        ]

    def get_court_reviews(self, obj):
        return [
            {
                "user": r.user.get_full_name(),
                "review_text": r.review_text,
                "rating": r.rating,
                "date_reviewed": r.date_reviewed,
            }
            for r in obj.reviews.all()
        ]