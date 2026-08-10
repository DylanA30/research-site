# This is an EXAMPLE of what your research_site/urls.py (the main
# project-level file, created automatically by `django-admin
# startproject`) should look like after you wire up the projects app.
# Copy the relevant lines into your actual research_site/urls.py.

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    # Anything starting with /projects/ gets handed off to
    # projects/urls.py to figure out the rest of the path
    path("projects/", include("projects.urls")),
]

# This block is ONLY needed during local development so Django will
# actually serve uploaded images from MEDIA_ROOT. In production, your
# web server (or a service like S3) handles this instead — Django
# itself doesn't serve media files efficiently at scale.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
