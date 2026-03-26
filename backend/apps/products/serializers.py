from rest_framework import serializers

from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False, allow_null=True)
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "description",
            "price",
            "image",
            "image_url",
            "created_at",
        ]

    def get_image_url(self, obj):
        request = self.context.get("request")

        if not obj.image:
            return None

        try:
            image_url = obj.image.url
        except Exception:
            return None

        if request:
            return request.build_absolute_uri(image_url)

        return image_url
