from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Questions, Answers, Learningspace, Comment

admin.site.register(User, UserAdmin)


class AnswerInline(admin.TabularInline):
    model = Answers


class QuestionsAdmin(admin.ModelAdmin):

    inlines = [AnswerInline]
    class Meta:
        model = Questions

class CommentInline(admin.StackedInline):
    model = Comment
    

class LearningspaceAdmin(admin.ModelAdmin):
    inlines = [CommentInline]
    class Meta:
        model = Comment

admin.site.register(Questions, QuestionsAdmin)
admin.site.register(Learningspace, LearningspaceAdmin)
admin.site.register(Answers)