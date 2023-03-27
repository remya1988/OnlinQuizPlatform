from django.contrib import admin
from .models import Quiz,Questions,Category,UserQuizAnswer

# Register your models here.
admin.site.register(Quiz)
admin.site.register(Questions)
admin.site.register(Category)
admin.site.register(UserQuizAnswer)
