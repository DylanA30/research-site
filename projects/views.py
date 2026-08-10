from django.shortcuts import render, get_object_or_404
from django.db.models import Q  # Q lets us build OR conditions in queries
from .models import Project, Tag

def home(request):
    from .models import NewsItem  # local import keeps this simple for now

    recent_news = NewsItem.objects.all()[:3]  # already ordered newest-first via Meta
    return render(request, "projects/home.html", {"recent_news": recent_news})

def project_list(request):
    """
    Shows all projects, with optional search and tag filtering via
    URL query parameters, e.g.:
        /projects/?q=neural
        /projects/?tag=nlp
        /projects/?q=neural&tag=nlp
    """
    # .all() starts with everything; we narrow it down step by step
    # below. Nothing hits the database until the queryset is actually
    # used (e.g. in the template) — this is called "lazy evaluation".
    projects = Project.objects.all()

    # request.GET is a dict-like object of URL query parameters.
    # .get("q") returns None if "q" isn't present, so this is safe
    # even if no search was performed.
    query = request.GET.get("q")
    if query:
        # Q objects let us say "title contains X OR summary contains X
        # OR description contains X". icontains = case-insensitive
        # "contains" match.
        projects = projects.filter(
            Q(title__icontains=query)
            | Q(summary__icontains=query)
            | Q(description__icontains=query)
        )

    tag_slug = request.GET.get("tag")
    if tag_slug:
        # __name filters on the related Tag model's "name" field
        # through the tags ManyToMany relationship
        projects = projects.filter(tags__name=tag_slug)

    context = {
        "projects": projects,
        "all_tags": Tag.objects.all(),  # used to render filter links
        "query": query or "",
        "active_tag": tag_slug or "",
    }
    return render(request, "projects/list.html", context)


def project_detail(request, slug):
    """
    Shows a single project's full detail page.
    get_object_or_404 automatically returns a 404 page if no project
    matches the slug, instead of crashing with an error.
    """
    project = get_object_or_404(Project, slug=slug)
    return render(request, "projects/detail.html", {"project": project})

def news_detail(request, slug):
    from .models import NewsItem
    item = get_object_or_404(NewsItem, slug=slug)
    return render(request, "projects/news_detail.html", {"item": item})