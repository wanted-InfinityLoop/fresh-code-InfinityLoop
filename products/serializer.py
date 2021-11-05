from rest_framework import serializers
from products.models import Category, Badge, Tag, Menu, Item

class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model  = Category
        fields = '__all__'
        
        
class BadgeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model  = Badge
        fields = '__all__'
        
        
class TagSerializer(serializers.ModelSerializer):
    
    class Meta:
        model  = Tag
        fields = '__all__'
        
        
class MenuSerializer(serializers.ModelSerializer):
    
    class Meta:
        model  = Menu
        fields = '__all__'
        
    
class ItemSerializer(serializers.ModelSerializer):
    
    class Meta:
        model  = Item
        fields = '__all__'