from rest_framework import serializers

class OwnerField(serializers.RelatedField):
    def to_representation(self, value):
        print("==================== internal value")
        return {
            'id': value.id,
            'first_name': value.first_name,
            'last_name': value.last_name,
        }

    def to_internal_value(self, data):
        return self.context['request'].user