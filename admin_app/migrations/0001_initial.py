# Generated by Django 5.0.4 on 2024-07-20 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BannerPhrase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phrase', models.CharField(blank=True, default=None, max_length=255, null=True)),
            ],
            options={
                'db_table': 'banner_phrase',
            },
        ),
    ]
