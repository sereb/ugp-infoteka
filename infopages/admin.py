from django.contrib import admin
from django import forms
from .models import *
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.contrib.admin import AdminSite
from django.contrib.auth.models import Group, User
from django.contrib.auth.admin import GroupAdmin, UserAdmin


class MyAdminSite(AdminSite):
    def get_app_list(self, request):
        """
        Return a sorted list of all the installed apps that have been
        registered in this site.
        """
        app_dict = self._build_app_dict(request)
        # Sort the apps alphabetically.
        app_list = sorted(app_dict.values(), key=lambda x: x['name'].lower())
        # Sort the models alphabetically within each app.
        # for app in app_list:
        #    app['models'].sort(key=lambda x: x['name'])
        return app_list


admin.site = MyAdminSite()


class AnswerAdmin(admin.StackedInline):
    model = Answer


class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerAdmin]
    list_filter = ('kursid',)
    search_fields = ['question', ]


class ResultAdmin(admin.ModelAdmin):
    list_filter = ('user',)

    def has_add_permission(self, request, obj=None):
        return False


class NaznAdmin(admin.ModelAdmin):
    list_filter = ('user',)


class StepAdmin(admin.ModelAdmin):
    list_display_links = ('title',)
    ordering = ('id',)
    list_display = ('order_number', 'title', 'kurseid',)
    list_filter = ('kurseid',)
    search_fields = ['title', ]


class KurseAdmin(admin.ModelAdmin):
    list_filter = ('catid',)
    search_fields = ['title', ]


class AnsAdmin(admin.ModelAdmin):
    list_filter = ('questionid',)
    search_fields = ['answer', ]


class ZadanAdmin (admin.ModelAdmin):
    list_filter = ('user',)
    list_display = ('user',)


admin.site.register(KCat)
admin.site.register(Kurse, KurseAdmin)
admin.site.register(Step, StepAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnsAdmin)
admin.site.register(Nazn, NaznAdmin)
admin.site.register(Zadanie, ZadanAdmin)
admin.site.register(Results, ResultAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(User, UserAdmin)
