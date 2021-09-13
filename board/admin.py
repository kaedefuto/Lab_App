from django.contrib import admin

# Register your models here.

from .models import BoardModel

#admin.site.register(SampleModel)
admin.site.register(BoardModel)