from rest_framework import serializers
from products.models import Group, Category, Product
from io import BytesIO
import os
from PIL import Image
import cloudinary
import cloudinary.uploader
import cloudinary.api
from cloudinary.exceptions import Error as CloudinaryError


class BaseSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    description = serializers.CharField(required=True)

    class Meta:
        fields = [
            'id',
            'name',
            'description',
        ]

    @staticmethod
    def validate_name(name):
        return name.strip().upper()

    @staticmethod
    def validate_description(description):
        return description.strip().capitalize()


class GroupSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = Group


class CategorySerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = Category


class ProductSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    description = serializers.CharField(required=True)
    price = serializers.IntegerField(required=True)
    stock = serializers.IntegerField(required=True)
    category = serializers.UUIDField(required=True)
    group = serializers.UUIDField(required=True)
    image = serializers.URLField(required=False, read_only=True)

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'description',
            'price',
            'stock',
            'image',
            'category',
            'group',
        ]

    @staticmethod
    def validate_name(name):
        return name.strip().upper()

    @staticmethod
    def validate_description(description):
        return description.strip().capitalize()

    def validate(self, attrs):
        if attrs['price'] < 0:
            raise serializers.ValidationError("El precio no puede ser negativo.")
        if attrs['stock'] < 0:
            raise serializers.ValidationError("El stock no puede ser negativo.")

        # We verify that the category exists
        try:
            Category.objects.get(id=attrs['category'])
        except Category.DoesNotExist:
            raise serializers.ValidationError("La categoría no existe.")

        # We verify that the group exists
        try:
            Group.objects.get(id=attrs['group'])
        except Group.DoesNotExist:
            raise serializers.ValidationError("El grupo no existe.")

        return attrs

    def create(self, validated_data):
        category = Category.objects.get(id=validated_data['category'])
        group = Group.objects.get(id=validated_data['group'])
        validated_data['category'] = category
        validated_data['group'] = group

        # Upload optimized image to Cloudinary
        image_file = self.context['request'].FILES.get('image_file')
        if image_file:
            try:
                # Open and process the image using Pillow
                image = Image.open(image_file)
                image = image.resize((320, 320))
                buffer = BytesIO()
                image.save(buffer, format='WEBP', optimize=True, quality=75)
                buffer.seek(0)

                # Upload optimized image to Cloudinary
                cloudinary.config(
                    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
                    api_key=os.getenv("CLOUDINARY_API_KEY"),
                    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
                )
                uploaded_image = cloudinary.uploader.upload(
                    file=buffer,
                    public_id=validated_data['name'],
                    folder="Products",
                    overwrite=True,
                    resource_type="image"
                )
                validated_data['image'] = uploaded_image['secure_url']
            except CloudinaryError:
                raise serializers.ValidationError(f"Error uploading image to Cloudinary")

        product = Product.objects.create(**validated_data)
        self.instance = product
        return product
