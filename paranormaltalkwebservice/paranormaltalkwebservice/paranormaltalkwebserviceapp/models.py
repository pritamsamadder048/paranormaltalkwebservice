from django.db import models
from django.core.validators import MaxValueValidator
import random
import hashlib
from datetime import datetime





def generate_hash():
    key = str(random.Random().randint(1, 10000))
    m = hashlib.sha1(bytes(key, encoding="UTF-8"))
    digest = m.hexdigest()
    return (key, digest)






def profile_picture_upload_location(instance,filename):
    return "%s/profile_image/%s"%(instance.service_name,filename)




class UserDetail(models.Model):

    full_name = models.CharField(max_length=500)

    email = models.EmailField(unique=True)
    mobile=models.CharField(max_length=20,blank=True,null=True)
    gender=models.CharField(max_length=8)
    #country = models.TextField();
    address=models.TextField(null=True,blank=True)
    key = models.CharField(max_length=40)
    password = models.CharField(max_length=200)
    user_createtime = models.DateTimeField(auto_now_add=True)
    profile_picture = models.ImageField(upload_to=profile_picture_upload_location,
                                        null=True,
                                        blank=True,
                                        height_field="height_field",
                                        width_field="width_field")
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    validemail = models.BooleanField(default=False)

    def __str__(self):
        return self.full_name

    def set_password(self, raw_password):
        self.key = str(random.Random().randint(1, 10000))

        m = hashlib.sha1(bytes(self.key, encoding="UTF-8"))
        m.update(bytes(raw_password, encoding="UTF-8"))
        self.password = m.hexdigest()
        # return password

    def check_password(self, raw_password):
        m = hashlib.sha1(bytes(self.key, encoding="UTF-8"))
        m.update(bytes(raw_password, encoding="UTF-8"))
        return m.hexdigest() == self.password


# UserSession Table
class UserSession(models.Model):
    full_name = models.CharField(max_length=500)
    email = models.EmailField(unique=True)
    mobile = models.CharField(blank=True,null=True,max_length=20)
    #User_Type=models.IntegerField()
    UserSession_starttime = models.DateTimeField(auto_now_add=True)
    UserSession_lastmodifiedtime = models.DateTimeField(auto_now=True)
    UserDetail_ref = models.OneToOneField(UserDetail, on_delete=models.CASCADE, primary_key=True)  # ,to_field='id')
    UserDetail_id = models.IntegerField(unique=True)
    UserSession_key = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.full_name

    def set_sessionkey(self):
        key = str(random.Random().randint(1, 10000))
        m = hashlib.sha1(bytes(key, encoding="UTF-8"))
        self.UserSession_key = m.hexdigest()

        return self.UserSession_key

    def check_sessionkey(self, clientsessionkey):
        return self.UserSession_key == clientsessionkey


class Post(models.Model):
    user_id=models.IntegerField()
    useretail_ref = models.ForeignKey(UserDetail, on_delete=models.CASCADE)
    user_full_name=models.CharField(max_length=500)
    post_createtime = models.DateTimeField(auto_now_add=True)
    post_details=models.TextField(blank=True,null=True)
    post_picture = models.ImageField(upload_to=profile_picture_upload_location,
                                        null=True,
                                        blank=True,
                                        height_field="height_field",
                                        width_field="width_field")
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    tot_like=models.IntegerField(default=0)

    def __str__(self):
        return self.user_full_name+" posted a status on : "+self.post_createtime

class Following(models.Model):

    user_id=models.IntegerField()
    userdetail_ref = models.ForeignKey(UserDetail, on_delete=models.CASCADE)
    user_full_name=models.CharField(max_length=500)

    following_id=models.IntegerField()
    followingdetail_ref = models.ForeignKey(UserDetail, on_delete=models.CASCADE)
    following_full_name=models.CharField(max_length=500)

    def __str__(self):
        return self.user_full_name+" Following  : "+self.following_full_name