from django.contrib import admin

from .models import Group, Post


class GroupAdmin(admin.ModelAdmin):
    list_display = ("pk", "title", "description", "slug")
    search_fields = ("title", "description" )
    list_filter = ("title",)
    empty_value_display = "-empty-"


class PostAdmin(admin.ModelAdmin):
    list_display = ("pk", "text", "pub_date", "author", "group")
    search_fields = ("text", )
    list_filter = ("pub_date", "author")
    empty_value_display = "-empty-"


admin.site.register(Group, GroupAdmin)
admin.site.register(Post, PostAdmin)
