# APIリクエストをモデルへ渡す役割。jsonのレスポンスを細かく制御する
from rest_framework import serializers
from .models import Category, Task, Profile
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        # 対象のクラス
        model = User
        # 制御をかけたい属性
        fields = ['id', 'username', 'password']
        # 細かな制御
        extra_kwargs = {'password': {'write_only': True, 'required': True}}

    # パスワードをハッシュ化して保存するため
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'user_profile', 'img']
        # profileはuser作成時に自動で作成するため、read_only
        extra_kwargs = {'user_profile': {'read_only': True}}


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'item']


class TaskSerializer(serializers.ModelSerializer):
    # 画面に返却したほうが使い勝手が良い項目を返却するため
    category_item = serializers.ReadOnlyField(source='category.item', read_only=True)
    owner_username = serializers.ReadOnlyField(source='owner.username', read_only=True)
    responsible_username = serializers.ReadOnlyField(source='responsible.username', read_only=True)
    # ModelのSTATUSに格納されている項目値を返却するため
    status_name = serializers.CharField(source='get_status_display', read_only=True)
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'task', 'description', 'criteria', 'status', 'status_name', 'category', 'category_item',
                  'estimate', 'owner', 'owner_username', 'responsible', 'responsible_username', 'created_at',
                  'updated_at']
        # Ownerはログインユーザに自動で割り当てるため
        extra_kwargs = {'owner': {'read_only': True}}