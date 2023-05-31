from rest_framework import serializers
from reviews.models import Review
from users.serializers import BasicUserSerializer

class ReviewSerializer(serializers.ModelSerializer):
    user = BasicUserSerializer()
    date = serializers.DateTimeField("%b %d, %Y")

    class Meta:
        model = Review
        fields = "__all__"