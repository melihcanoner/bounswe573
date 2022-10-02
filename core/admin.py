from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Questions, Answers

admin.site.register(User, UserAdmin)


class AnswerInline(admin.TabularInline):
    model = Answers


class QuestionsAdmin(admin.ModelAdmin):

    inlines = [AnswerInline]
    class Meta:
        model = Questions


admin.site.register(Questions, QuestionsAdmin)

admin.site.register(Answers)