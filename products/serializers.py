from django.db.models.deletion import ProtectedError
from rest_framework import serializers

from products.models import Group, Category, Product
from io import BytesIO
import os
from PIL import Image
import cloudinary
import cloudinary.uploader
import cloudinary.api
from cloudinary.exceptions import Error as CloudinaryError


class BaseCreateSerializer(serializers.ModelSerializer):

    @staticmethod
    def validate_name(name):
        return name.strip().upper()

    @staticmethod
    def validate_description(description):
        return description.strip().capitalize()

    def validate(self, attrs):
        if self.Meta.model.objects.filter(name=attrs['name']).exists():
            raise serializers.ValidationError(self.name_error)
        return attrs

    def create(self, validated_data):
        return self.Meta.model.objects.create(**validated_data)


class CreateGroupSerializer(BaseCreateSerializer):
    name_error = "Ya hay un grupo con este nombre"

    class Meta:
        model = Group
        fields = [
            'id',
            'name',
            'description',
        ]


class CreateCategorySerializer(BaseCreateSerializer):
    name_error = "Ya hay una categoría con este nombre"

    class Meta:
        model = Category
        fields = [
            'id',
            'name',
            'description',
        ]


class BaseUpdateSerializer(serializers.ModelSerializer):

    @staticmethod
    def validate_name(name):
        return name.strip().upper()

    @staticmethod
    def validate_description(description):
        return description.strip().capitalize()

    def validate(self, attrs):
        if not self.instance or not self.Meta.model.objects.filter(id=self.instance.id).exists():
            raise serializers.ValidationError(self.object_error)
        if self.Meta.model.objects.filter(name=attrs['name']).exclude(id=self.instance.id).exists():
            raise serializers.ValidationError(self.name_error)
        return super().validate(attrs)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance


class UpdateGroupSerializer(BaseUpdateSerializer):
    object_error = "Grupo no encontrado"
    name_error = "Ya hay un grupo con este nombre"

    class Meta:
        model = Group
        fields = [
            'id',
            'name',
            'description',
        ]


class UpdateCategorySerializer(BaseUpdateSerializer):
    object_error = "Categoría no encontrada"
    name_error = "Ya hay una categoría con este nombre"

    class Meta:
        model = Category
        fields = [
            'id',
            'name',
            'description',
        ]


class DeleteGroupSerializer(serializers.Serializer):
    group_id = serializers.UUIDField(required=True)

    def validate(self, attrs):
        try:
            self.instance = Group.objects.get(id=attrs['group_id'])
        except Group.DoesNotExist:
            raise serializers.ValidationError("Grupo no encontrado")
        return attrs

    def delete(self):
        try:
            self.instance.delete()
        except ProtectedError:
            raise serializers.ValidationError("El grupo no puede ser eliminado porque tiene productos asociados")


class DeleteCategorySerializer(serializers.Serializer):
    category_id = serializers.UUIDField(required=True)

    def validate(self, attrs):
        try:
            self.instance = Category.objects.get(id=attrs['category_id'])
        except Category.DoesNotExist:
            raise serializers.ValidationError("Categoría no encontrada")
        return attrs

    def delete(self):
        try:
            self.instance.delete()
        except ProtectedError:
            raise serializers.ValidationError("La categoría no puede ser eliminada porque tiene productos asociados")


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
