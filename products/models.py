import uuid

from django.db import models


class BaseEntity(models.Model):
    """
    Base model for Group and Category

    This model contains the common attributes shared by Group and Category.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, blank=False, null=False, editable=False)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    class Meta:
        abstract = True


class Group(BaseEntity):
    """
    Group model

    This model represents a group of products. For example, for BTS products, the group would be "BTS",
    and the products would be the albums, posters, etc.
    """

    class Meta:
        db_table = "group"


class Category(BaseEntity):
    """
    Category model

    This model represents a category of products. For example, for BTS products, the category would be "Albums",
    "Photo Cards", etc.
    """

    class Meta:
        db_table = "category"


class BaseProduct(models.Model):
    """
    Base model for Product and Version

    This model contains the common attributes shared by Product and Version.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, blank=False, null=False, editable=False)
    name = models.CharField(max_length=100)
    stock = models.IntegerField(default=0, blank=True, null=True)
    image = models.URLField(default=None, blank=True, null=True)
    is_disabled = models.BooleanField(default=False, blank=True, null=True)

    class Meta:
        abstract = True


class Product(BaseProduct):
    """
    Product model

    This model represents a product. For example if the product is an album, the product would be "Map of the Soul: 7".
    The category would be "Albums" and the group would be "BTS".

    Attributes:
        - is_disabled: BooleanField to indicate if the product is sold out or not
    """
    description = models.TextField(blank=True, null=True)
    price = models.IntegerField(default=0, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    group = models.ForeignKey(Group, on_delete=models.PROTECT)
    discount_price = models.IntegerField(blank=True, null=True, default=None)

    class Meta:
        db_table = "product"


class Version(BaseProduct):
    """
    Version model

    This model represents a version of a product. For example, if the product is an album, the versions would be
    "Version 1", "Version 2", etc.
    """
    product = models.ForeignKey(Product, on_delete=models.PROTECT)

    class Meta:
        db_table = "version"


class ProductImageFile(models.Model):
    """
    ProductImageFile model

    This model represents images of a product
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, blank=False, null=False, editable=False)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    image = models.URLField()

    class Meta:
        db_table = "product_image_file"
