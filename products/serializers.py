from django.db.models.deletion import ProtectedError
from rest_framework import serializers

from products.models import Group, Category, Product, ProductImageFile, Version
import os
import cloudinary
import cloudinary.uploader
import cloudinary.api

from products.utils import upload_image_to_cloudinary


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
            url = upload_image_to_cloudinary(
                image_file=image_file,
                folder="Products",
            )
            validated_data['image'] = url
        product = Product.objects.create(**validated_data)
        self.instance = product
        return product

    def update(self, instance, validated_data):
        old_name = instance.name
        new_name = validated_data.get('name', instance.name)

        if old_name != new_name and instance.image:
            try:
                cloudinary.config(
                    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
                    api_key=os.getenv("CLOUDINARY_API_KEY"),
                    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
                )

                image_url = instance.image
                parts = image_url.split('/')
                public_id_with_folder = '/'.join(parts[7:]).split('.')[0]
                new_public_id = f"Products/{new_name}"

                response = cloudinary.uploader.rename(
                    from_public_id=public_id_with_folder,
                    to_public_id=new_public_id,
                    folder="Products"
                )

                new_image_url = response['secure_url']
                validated_data['image'] = new_image_url

            except cloudinary.exceptions.Error as e:
                raise serializers.ValidationError('Ocurrió un error al intentar actualizar la imagen')

        category_id = validated_data.get('category')
        group_id = validated_data.get('group')

        if category_id and category_id != instance.category.id:
            category = Category.objects.get(id=category_id)
            instance.category = category

        if group_id and group_id != instance.group.id:
            group = Group.objects.get(id=group_id)
            instance.group = group

        for attr, value in validated_data.items():
            if attr not in ['category', 'group']:
                setattr(instance, attr, value)

        instance.save()
        return instance


class ProductImageFileSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=True)

    class Meta:
        model = ProductImageFile
        fields = [
            'id',
            'image',
        ]

    def validate(self, attrs):
        product_id = self.context['product_id']
        try:
            Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            raise serializers.ValidationError("El producto no existe.")
        return attrs

    def create(self, validated_data):
        product_id = self.context['product_id']
        product = Product.objects.get(id=product_id)
        validated_data['product'] = product
        folder_name = f"Products/ProductsImages"
        image = validated_data['image']
        if image:
            url = upload_image_to_cloudinary(
                image_file=image,
                folder=folder_name,
            )
            validated_data['image'] = url
        product_image = ProductImageFile.objects.create(**validated_data)
        self.instance = product_image
        return product_image


class VersionSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    stock = serializers.IntegerField(required=True)
    image = serializers.ImageField(required=True)

    class Meta:
        model = Version
        fields = [
            'id',
            'name',
            'stock',
            'image',
        ]

    @staticmethod
    def validate_name(name):
        return name.strip().upper()

    def validate(self, attrs):
        stock = attrs.get('stock')
        product_id = self.context.get('product_id')

        if stock < 0:
            raise serializers.ValidationError("El stock no puede ser negativo.")

        try:
            Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            raise serializers.ValidationError("El producto no existe.")
        return attrs

    def create(self, validated_data):
        product_id = self.context.get('product_id')
        product = Product.objects.get(id=product_id)
        validated_data['product'] = product
        folder_name = f"Products/ProductsVersions"
        image = validated_data['image']
        if image:
            url = upload_image_to_cloudinary(
                image_file=image,
                folder=folder_name,
            )
            validated_data['image'] = url
        version = Version.objects.create(**validated_data)
        self.instance = version
        return version
