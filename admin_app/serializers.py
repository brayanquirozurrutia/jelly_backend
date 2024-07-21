from rest_framework import serializers
from admin_app.models import BannerPhrase
from django.core.cache import cache


class BannerPhraseSerializer(serializers.ModelSerializer):
    class Meta:
        model = BannerPhrase
        fields = [
            'id',
            'phrase',
        ]

    @staticmethod
    def validate_phrase(phrase):
        return phrase.strip().upper()

    def validate(self, attrs):
        phrase = attrs['phrase']

        if cache.get(f'banner_phrase_{phrase}'):
            raise serializers.ValidationError('La frase ya existe')

        if len(phrase) > 255:
            raise serializers.ValidationError('La frase no puede tener más de 255 caracteres')
        elif len(phrase) < 1:
            raise serializers.ValidationError('La frase no puede estar vacía')

        return attrs

    def create(self, validated_data):
        quantity = cache.get('banner_phrase_count')

        if quantity is None:
            quantity = BannerPhrase.objects.count()
            cache.set('banner_phrase_count', quantity)

        if quantity < 10:
            instance = BannerPhrase.objects.create(**validated_data)
            phrase = validated_data['phrase']
            cache.set(f'banner_phrase_{phrase}', True)
            cache.set('banner_phrase_count', quantity + 1)
            return instance
        else:
            raise serializers.ValidationError('No se pueden agregar más de 10 frases')

    def update(self, instance, validated_data):

        new_phrase = validated_data.get('phrase', '')
        old_phrase = instance.phrase

        if old_phrase != new_phrase:
            cache.delete(f'banner_phrase_{old_phrase}')
            if cache.get(f'banner_phrase_{new_phrase}'):
                raise serializers.ValidationError('La nueva frase ya existe')

        instance.phrase = new_phrase
        instance.save()

        cache.set(f'banner_phrase_{new_phrase}', True)
        return instance

    def destroy(self, instance):
        phrase = instance.phrase
        instance.delete()
        cache.delete(f'banner_phrase_{phrase}')
        quantity = cache.get('banner_phrase_count', 0)
        print(quantity)
        cache.set('banner_phrase_count', quantity - 1)
