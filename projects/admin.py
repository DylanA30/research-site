from django.contrib import admin
from .models import Project, Tag, ProjectImage, NewsItem
admin.site.register(Tag)


class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1
    fields = ("image", "video", "caption", "category", "order",)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "status", "created_at")
    list_filter = ("status", "tags")
    search_fields = ("title", "summary", "description")
    filter_horizontal = ("tags",)
    prepopulated_fields = {"slug": ("title",)}
    inlines = [ProjectImageInline]

@admin.register(NewsItem)
class NewsItemAdmin(admin.ModelAdmin):
    list_display = ("title", "date")
    filter_horizontal = ("tags",)