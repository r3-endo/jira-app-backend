from rest_framework import permissions


# リソースに対するユーザーのCRUD制約を設ける
class OwnerPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        # Getリクエストの場合は制約を設けない。それ以外は自らのタスクのみ更新できる
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner.id == request.user.id
