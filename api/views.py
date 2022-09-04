# モデルと連携してJSON形式のレスポンスを作成する。ユーザに提示するデータ内容を記述する。
# genericsViewは特定の操作に特化した制約。ViewSetはModelに対する操作全般の制約。
from django.shortcuts import render
from rest_framework import status, permissions, generics, viewsets
from .serializers import UserSerializer, ProfileSerializer, CategorySerializer, TaskSerializer
from rest_framework.response import Response
from .models import Task, Category, Profile
from django.contrib.auth.models import User
from . import custompermissions


# 新規ユーザ作成
# Create専用のエンドポイント
# ユーザの作成、取得、ログインユーザの取得（Userモデル）に対する操作は別のクラスで管理するため、genericsのAPIViewを使用
class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer
    # 登録時は誰でもアクセスできるようpermissionを変えておく必要があるため
    permission_classes = (permissions.AllowAny,)


# ユーザリスト取得
# Read-Onlyのエンドポイント
# モデルインスタンスをコレクションとして出力
class ListUserView(generics.ListAPIView):
    # Userオブジェクトを全て取得
    queryset = User.objects.all()
    serializer_class = UserSerializer


# ログインユーザ取得
# Read-Onlyのエンドポイント
# Keyに紐づくモデルインスタンスを出力
class LoginUserView(generics.RetrieveAPIView):
    serializer_class = UserSerializer

    # ログインしているユーザを返却するため
    def get_object(self):
        return self.request.user

    # 使用しないCRUDを無効化しておく
    def update(self, request, *args, **kwargs):
        response = {'message': 'PUT method is not Allowed'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


# プロフィールの作成/更新
# Modelに対するCRUD操作を１つのクラスにまとめるためViewSetを使用
class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    # フロントエンドからプロフィールを指定しなくてもログインしているユーザを特定できるようにするため
    # ログインユーザのプロフイールを格納する
    def perform_create(self, serializer):
        serializer.save(user_profile=self.request.user)

    # 使用しないCRUDを無効化しておく
    def destroy(self, request, *args, **kwargs):
        response = {'message': 'DELETE method is not Allowed'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        response = {'message': 'PATCH method is not Allowed'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


# カテゴリーの新規作成
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    # 使用しないCRUDを無効化しておく
    def destroy(self, request, *args, **kwargs):
        response = {'message': 'DELETE method is not Allowed'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        response = {'message': 'UPDATE method is not Allowed'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        response = {'message': 'PATCH method is not Allowed'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


# タスクの新規作成/更新
class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    # タスクは自身が作成したもの以外は更新できないようにするため
    permission_classes = (permissions.IsAuthenticated, custompermissions.OwnerPermission)

    # タスクを生成したときにオーナーをカテゴリー作成者に割り当てるため
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    # 使用しないCRUDを無効化しておく
    def partial_update(self, request, *args, **kwargs):
        response = {'message': 'PATCH method is not Allowed'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)