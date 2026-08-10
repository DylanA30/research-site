from django.db import models
from django.utils.text import slugify
from cloudinary_storage.storage import VideoMediaCloudinaryStorage


# -----------------------------------------------------------------------
# Tag model
# -----------------------------------------------------------------------
# We give tags their own model (instead of just a text field) so that:
#   1. We can filter projects by tag cleanly in a URL, e.g. ?tag=nlp
#   2. Each tag is stored once and reused, instead of duplicated text
#      like "Machine Learning" vs "machine learning" causing mismatches
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        # __str__ controls what shows up in the Django admin dropdowns
        # and anywhere you print/display this object
        return self.name


# -----------------------------------------------------------------------
# Project model
# -----------------------------------------------------------------------
# This is the main model. Each independent research project you add
# becomes one row in the database, editable via /admin.
class Project(models.Model):

    # Lets you mark a project's stage. choices= restricts the admin
    # dropdown to only these options, preventing typos like "Ongong"
    STATUS_CHOICES = [
        ("planning", "Planning"),
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
        ("paused", "Paused"),
    ]

    title = models.CharField(max_length=200)

    # slug = URL-friendly version of the title, e.g. "My Cool Project"
    # becomes "my-cool-project". Used to build clean detail page URLs
    # like /projects/my-cool-project/ instead of /projects/1/
    slug = models.SlugField(max_length=220, unique=True, blank=True)

    # Short one/two-liner shown on the project list page
    summary = models.CharField(max_length=300)

    # Full write-up shown on the project's own detail page.
    # TextField = no length limit, unlike CharField
    description = models.TextField()

    # ---- IMAGE SUPPORT ----
    # ImageField stores an uploaded image and saves it under MEDIA_ROOT
    # (configured in settings.py). Requires the 'Pillow' package
    # (pip install Pillow) since Django uses it to validate images.
    # blank=True / null=True means the field is optional — not every
    # project needs a cover image.
    cover_image = models.ImageField(
        upload_to="project_covers/",  # subfolder inside MEDIA_ROOT
        blank=True,
        null=True,
    )

    # ManyToMany because one project can have several tags, and one
    # tag (e.g. "python") can apply to many projects
    tags = models.ManyToManyField(Tag, blank=True, related_name="projects")

    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="in_progress"
    )

    # Optional link out to a paper, GitHub repo, dataset, etc.
    external_link = models.URLField(blank=True)

    # auto_now_add sets this ONCE when the row is first created
    created_at = models.DateTimeField(auto_now_add=True)

    # auto_now updates this EVERY time the row is saved
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # Default ordering whenever you query Project.objects.all()
        # "-created_at" = newest first (the minus sign means descending)
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Auto-generate the slug from the title if one wasn't set manually.
        # This runs every time you save a Project in the admin.
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

# -----------------------------------------------------------------------
# ProjectImage model
# -----------------------------------------------------------------------
# A separate model for extra images, linked back to Project via a
# ForeignKey. This is how Django handles "one thing has many images" —
# each row here is ONE image that belongs to ONE project, but a
# project can have many of these rows pointing at it.
class ProjectImage(models.Model):

    CATEGORY_CHOICES = [
        ("process", "Process Photo"),
        ("results", "Data / Results"),
    ]

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="images",
    )
    image = models.ImageField(upload_to="project_gallery/", blank=True, null=True)
    video = models.FileField(
        upload_to="project_gallery/videos/",
        storage=VideoMediaCloudinaryStorage(),
        blank=True,
        null=True,
    )
    caption = models.CharField(max_length=600, blank=True)
    order = models.PositiveIntegerField(default=0)
    category = models.CharField(
        max_length=20, choices=CATEGORY_CHOICES, default="process"
    )

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"Image for {self.project.title}"

# -----------------------------------------------------------------------
# NewsItem model
# -----------------------------------------------------------------------
# Short update cards for the homepage "Recent News" section — things
# like "Started a new project" or "Published results." You'll add,
# edit, and remove these through /admin/ as things happen.
class NewsItem(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    image = models.ImageField(upload_to="news/", blank=True, null=True)
    tags = models.ManyToManyField(Tag, blank=True, related_name="news_items")
    date = models.DateField()

    # Full write-up shown on the news item's own detail page
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

