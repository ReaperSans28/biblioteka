from rest_framework import serializers


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            "id",
            "title",
            "author",
            "description",
            "isbn",
            "year_published",
            "pages",
            "cover_image",
            "cover_image_url",
            "created_at",
            "updated_at",
        )
        read_only_fields = ["id", "created_at", "updated_at"]

    def get_cover_image_url(self, obj):
        """
        Метод для получения полного URL изображения обложки.

        obj - это экземпляр модели Book

        Если изображение есть, возвращаем полный URL.
        Если нет - возвращаем None.
        """
        if obj.cover_image:
            request = self.context.get("request")
            if request:
                return request.build_absolute_uri(obj.cover_image.url)
            return obj.cover_image.url
        return None
