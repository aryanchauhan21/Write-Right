from django.shortcuts import render
from src.mixed.models import Questions
from src.blog.models import BlogPost
from operator import attrgetter
from src.blog.views import get_blog_queryset
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

NO_OF_POSTS_PER_PAGE = 5
# Create your views here.


def home_screen_view(request):
    context = {}
    query = request.GET.get('q', '')
    context['query'] = str(query)

    blog_posts = sorted(get_blog_queryset(query), key=attrgetter('date_updated'), reverse=True)

    # Pagination
    page = request.GET.get('page', 1)
    blog_posts_paginator = Paginator(blog_posts, NO_OF_POSTS_PER_PAGE)

    try:
        blog_posts = blog_posts_paginator.page(page)
    except PageNotAnInteger:
        blog_posts = blog_posts_paginator.page(NO_OF_POSTS_PER_PAGE)
    except Paginator:
        blog_posts = blog_posts_paginator.page(blog_posts_paginator.num_pages)

    context['blog_posts'] = blog_posts
    return render(request, 'mixed/home.html', context)


# def mixed_home_view(request):
#     print(request.headers)
#     return render(request, "mixed/home.html", {})
#
# def mixed_2(request):
#     context = {}
#     context['Developer_Name'] = "Aryan Chauhan"
#     demoItemList = ["item1", "item2", "item3", "item4"]
#     context['demoItemList'] = demoItemList
#     return render(request, "mixed/home2.html", context)
#
#
# def show_questions(request):
#     context = {}
#     questions = Questions.objects.all()
#     context['questions'] = questions
#     return render(request, 'mixed/show_questions.html', context)
#
