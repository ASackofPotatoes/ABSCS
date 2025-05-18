from rest_framework import serializers
from page.models import Page, Mnemonic, Command

class MnemonicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mnemonic
        fields = '__all__'
        
class CommandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Command
        fields = ['id', 'name', 'encoding_type', 'content']
    
    def get_content(self, obj):
        return obj.content.decode('ascii') if obj.encoding_type == 'Binary' else obj.content
    
    def create(self, validated_data):
        content = self.initial_data.get('command_content')
        encoding_type = validated_data['encoding_type']
        name = validated_data['name']

        instance = Command(name=name, encoding_type=encoding_type)
        instance.set_content(content)
        instance.save()
        return instance
    
    def update(self, instance, validated_data):
        content = self.initial_data.get('command_content', None)

        if 'name' in validated_data:
            instance.name = validated_data['name']
        if 'encoding_type' in validated_data:
            instance.encoding_type = validated_data['encoding_type']
        if content is not None:
            instance.set_content(content)

        instance.save()
        return instance
