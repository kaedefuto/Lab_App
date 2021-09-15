from django.contrib import admin

# Register your models here.

from .models import BoardModel
from .models import ThreadModel

#admin.site.register(SampleModel)
admin.site.register(BoardModel)
admin.site.register(ThreadModel)