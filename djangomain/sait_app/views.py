from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseForbidden
from django.urls import reverse, reverse_lazy
from django.core.exceptions import PermissionDenied
from django.db.models.query_utils import Q
from django.views import defaults
from django.template.loader import render_to_string
from datetime import datetime
from sait_app.models import Author, Publisher, Tag
# RegisteredUsers
# from fast_app1.form import RegisterForm
from django.views.generic import TemplateView, ListView, FormView, DetailView

from sait_app.utils import DataMixin


class HomeView(DataMixin, ListView):
    model = Author
    template_name = 'sait_app/home.html'
    context_object_name = 'author_table'
    paginate_by = 5
    title_page = 'home page'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = self.plus_mixin_data(context, **kwargs)
        # context['title'] = 'home page'
        return context

    # def home(self, request):
    #     author_table = Author.objects_authormanager.all()
    #     context = {
    #         'title': "home page",
    #         'author_table': author_table,
    #     }
    #     return render(request, template_name='fast_app1/home.html', context=context)


# ----------------------------------------------
class PublisherSlugView(DataMixin, ListView):
    model = Publisher
    context_object_name = 'select_author'
    template_name = 'sait_app/publisher_slug.html'
    paginate_by = 3

    def __init__(self):
        super().__init__()
        self.publisher_object = None
        self.publisher_slug = None

    def get_queryset(self):
        self.publisher_slug = self.kwargs['publisher_slug']
        self.publisher_object = get_object_or_404(Publisher, slug=self.publisher_slug)
        return self.publisher_object.author.all().prefetch_related('publisher')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['title'] = 'publisher_' + self.publisher_slug
        context['publisher_object'] = self.publisher_object
        context['publisher_name'] = self.publisher_object.publisher_name
        context['publisher_content'] = self.publisher_object.publisher_content
        context = self.plus_mixin_data(context, title='publisher_' + self.publisher_slug)
        return context


# def publisher_slug(request, publisher_slug):
#     publisher_object = get_object_or_404(Publisher, slug=publisher_slug)
#     select_author = publisher_object.author.all().prefetch_related('publisher')
#     context = {
#         'publisher_object': publisher_object,
#         'publisher_name': publisher_object.publisher_name,
#         'select_author': select_author,
#         'title': 'издатели',
#     }
#     return render(request, 'fast_app1/publisher_slug.html', context=context)


# ----------------------------------------------

class AuthorSlugView(LoginRequiredMixin, DataMixin, DetailView):
    # template_name_field = ''
    login_url = "/users/login/"
    # redirect_field_name = "redirect_to"
    template_name = 'sait_app/author_slug.html'
    model = Author
    context_object_name = 'author_objects'
    slug_url_kwarg = 'author_slug'
    slug_field = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = self.plus_mixin_data(context, title='author_' + self.kwargs['author_slug'])
        return context


# def author_slug(request, author_slug):
#     author_objects = get_object_or_404(Author, slug=author_slug)
#     context = {
#         'name_slug': author_slug,
#         'title': 'author_slug',
#         'author_objects': author_objects,
#      }
#     return render(request, template_name='fast_app1/author_slug.html', context=context)


# ----------------------------------------------
class TagSlugView(DataMixin, ListView):
    model = Tag
    context_object_name = 'select_author'
    template_name = 'sait_app/tag_slug.html'
    paginate_by = 3

    def __init__(self):
        super().__init__()
        self.tag_slug = None
        self.tag_objects = None

    def get_queryset(self):
        self.tag_slug = self.kwargs['tag_slug']
        self.tag_objects = get_object_or_404(Tag, slug=self.tag_slug)
        return Author.objects_authormanager.filter(tag_id=self.tag_objects.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['title'] = 'tag_' + self.tag_slug
        context['tag_objects'] = self.tag_objects
        context['tag_name'] = self.tag_objects.tag
        context = self.plus_mixin_data(context, title='tag_' + self.tag_slug)
        return context


# def tag_slug(request, tag_slug):
#     tag_objects = get_object_or_404(Tag, slug=tag_slug)
#     tag_name = tag_objects.tag
#     select_author = Author.objects_authormanager.filter(tag_id=tag_objects.pk)
#     context = {
#         'title': 'tag_slug',
#         'tag_objects': tag_objects,
#         'tag_name': tag_name,
#         'select_author': select_author,
#     }
#     return render(request, 'fast_app1/tag_slug.html', context=context)


# ----------------------------------------------
# class RegisterPageView(DataMixin, FormView):
#     template_name = 'fast_app1/register_page.html'
#     form_class = RegisterForm
#     success_url = reverse_lazy('home')
#     extra_context = {'title': 'register page', }
#     prefix = ''
#     title_page = 'register page'
#
#     def form_valid(self, form):
#         if form.is_valid():
#             form.save()
#         return super().form_valid(form)
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context = self.plus_mixin_data(context)
#         return context

# def register_page(request):
#     form = None
#     if request.method == 'GET':
#         form = RegisterForm()
#     elif request.method == 'POST':
#         form = RegisterForm(request.POST, request.FILES)
#         if form.is_valid():
#             load_file = request.FILES.get('photo_user', False)
#             if load_file:
#                 # uploaded_file(load_file)
#                 form.save()
#                 return redirect('home')
#             form.add_error(field='photo_user', error='выбрать файл')
#
#     context = {
#         'title': 'register_page',
#         'form': form,
#     }
#     return render(request, 'fast_app1/register_page.html', context=context)


# ----------------------------------------------
def contact(request):
    context = {
        'title': 'contact',
    }
    return render(request, template_name='sait_app/contact.html', context=context)


# ----------------------------------------------
def news(request):
    context = {
        'title': 'news',
    }
    return render(request, template_name='sait_app/news.html', context=context)


# ----------------------------------------------
def chat(request):
    context = {
        'title': 'chat',
    }
    return render(request, template_name='sait_app/chat.html', context=context)


# ----------------------------------------------
def about_repath(request, year):
    if int(year) > 2024:
        raise Http404()
        # raise PermissionDenied
    return HttpResponse("<h1>СТРАНИЦА ABOUT_repath</h1><p>year: {}</p>".format(year))


# ----------------------------------------------
def list_notfound(request, exception):
    return HttpResponseNotFound("<h1>СТРАНИЦА HTTP RESPONSE NOT FOUND 404</h1>")


# ----------------------------------------------
def eror_403(request, exception):
    return HttpResponseForbidden("<h1>СТРАНИЦА HTTP RESPONSE NOT FOUND 403</h1>")


# ----------------------------------------------
def uploaded_file(load_file):
    with open(f'media/photo_users/{load_file.name}', "wb+") as destination:
        for chunk in load_file.chunks():
            destination.write(chunk)
