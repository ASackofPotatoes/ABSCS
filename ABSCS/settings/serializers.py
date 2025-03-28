from rest_framework import serializers
from page.models import Page, Mnemonic

class MnemonicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mnemonic
        fields = '__all__'
