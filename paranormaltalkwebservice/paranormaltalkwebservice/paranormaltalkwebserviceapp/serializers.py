from rest_framework import serializers


from  .models import UserDetail
from .models import UserSession
from .models import Following
from .models import Post





#User Detail serializer
class UserDetailSerializer(serializers.ModelSerializer):


    class Meta:
        model=UserDetail
        fields=("id","full_name","email","mobile","address","user_createtime",)


class FollowingSerializer(serializers.ModelSerializer):


    class Meta:
        model=Following
        fields="__all__"


class PostSerializer(serializers.ModelSerializer):


    class Meta:
        model=Post
        fields="__all__"

