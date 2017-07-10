from django.contrib import admin

from .models import UserDetail
from .models import UserSession



admin.site.register(UserDetail)
admin.site.register(UserSession)
