from django import forms
from django.db import models

from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index

import datetime
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import get_template

from wagtail.search.backends import get_search_backend

from wagtail.core.fields import StreamField
from wagtail.core import blocks
from wagtail.admin.edit_handlers import StreamFieldPanel
from wagtail.images.blocks import ImageChooserBlock
from wagtail.embeds.blocks import EmbedBlock

from blog.blocks import TwoColumnBlock, ThreeColumnBlock, ImageLeftBlock, ImageCenterBlock
from blog.tools import PageTree

from wagtail.snippets.models import register_snippet

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from wagtail.core.models import Page

POSTS_ON_PAGE = 3

# Create your models here.

#def set_cookie(response, key, value, days_expire = 7):
#    if days_expire is None:
#        max_age = 365 * 24 * 60 * 60  #one year
#    else:
#        max_age = days_expire * 24 * 60 * 60 
#    expires = datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age), "%a, %d-%b-%Y %H:%M:%S GMT")
#    response.set_cookie(key, value, max_age=max_age, expires=expires, domain=settings.SESSION_COOKIE_DOMAIN, secure=settings.SESSION_COOKIE_SECURE or None


def setContext(context):
    #latest posts
    index = BlogIndexPage.objects.filter(title='Posts')[0]
    #                                                    -first_published_at
    latest_posts = index.get_children().live().order_by('-last_published_at')[:5]
    context['latest_posts'] = latest_posts

def pageLimits(nr_posts):
    global POSTS_ON_PAGE
    limits = []
    intervals = []
    n = 0
    while True:
        #print(n)
        limits.append(n)
        n += POSTS_ON_PAGE
        if(n >= nr_posts):
            break
    if(n > nr_posts): 
        n = nr_posts
        #print(n)
        limits.append(n)
    #print(limits)
    l = len(limits)
    for i in range(l-1):
        interval = limits[i:i+2]
        intervals.append(interval)
    #print(intervals)
    return intervals


class BlogIndexPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full")
    ]

    def get_context(self, request, *args, **kwargs):
        """Adding custom stuff to our context."""
        context = super().get_context(request, *args, **kwargs)
        # Get all posts
        all_posts = BlogPage.objects.live().public().order_by('-first_published_at')

        # Paginate all posts by 3 per page
        paginator = Paginator(all_posts, 3)
        # Try to get the ?page=x value
        page = request.GET.get("page")
        try:
            # If the page exists and the ?page=x is an int
            posts = paginator.page(page)
        except PageNotAnInteger:
            # If the ?page=x is not an int; show the first page
            posts = paginator.page(1)
        except EmptyPage:
            # If the ?page=x is out of range (too high most likely)
            # Then return the last page
            posts = paginator.page(paginator.num_pages)

        # "posts" will have child pages; you'll need to use .specific in the template
        # in order to access child properties, such as youtube_video_id and subtitle
        context["posts"] = posts
        setContext(context)
        return context


class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey(
        'BlogPage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )

class BlogPage(Page):
    date = models.DateField("Post date")
    intro = models.CharField(max_length=250)
    #body = RichTextField(blank=True)
    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)
    categories = ParentalManyToManyField('blog.BlogCategory', blank=True)

    body = StreamField([
        ('heading', blocks.CharBlock(classname="full title")),
        ('paragraph', blocks.RichTextBlock()),
        ('two_columns', TwoColumnBlock()),
        ('three_columns', ThreeColumnBlock()),
        ('image_center', ImageCenterBlock()),
        ('image_left', ImageLeftBlock()),
        ('video', EmbedBlock(icon="media")),
        ('htmljs', blocks.TextBlock(icon="cog")),
        ('code_bash', blocks.TextBlock(icon="code")),
        ('code_py', blocks.TextBlock(icon="code")),
        ('code_htmljs', blocks.TextBlock(icon="code")),
        ],null=True,blank=True)

    def main_image(self):
        gallery_item = self.gallery_images.first()
        if gallery_item:
            return gallery_item.image
        else:
            return None

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        InlinePanel('gallery_images', label="Gallery images-Main image"),    
        MultiFieldPanel([
            FieldPanel('date'),
            FieldPanel('tags'),
            FieldPanel('categories', widget=forms.CheckboxSelectMultiple),
        ], heading="Blog information"),
        FieldPanel('intro'),
        #FieldPanel('body'),
        StreamFieldPanel('body'),
        #InlinePanel('gallery_images', label="Gallery images"),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        setContext(context)
        return context


class BlogPageGalleryImage(Orderable):
    page = ParentalKey(BlogPage, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )
    caption = models.CharField(blank=True, max_length=250)

    panels = [
        ImageChooserPanel('image'),
        FieldPanel('caption'),
    ]


class BlogTagIndexPage(Page):

    def get_context(self, request):

        # Filter by tag
        tag = request.GET.get('tag')
        blogpages = BlogPage.objects.filter(tags__name=tag)

        # Update template context
        context = super().get_context(request)
        context['blogpages'] = blogpages
        setContext(context)
        return context

class BlogAllTags(Page):
    def get_context(self, request):
        tagList = []
        tags = BlogPageTag.objects.all()
        #tags = BlogPageTag.objects.order_by("tag")
        for tag in tags:
            if tag.tag.name not in tagList:
                tagList.append(tag.tag.name)
        tagList.sort()

        context = super().get_context(request)
        context['tags'] = tagList   
        setContext(context)
        return context

class BlogAllCategories(Page):
    def get_context(self, request):
        context = super().get_context(request)
        categories = BlogCategory.objects.all()
        context['categories'] = categories
        setContext(context)
        return context    

class BlogSearch(Page):
    def get_context(self, request):
        word = request.GET.get('key')
        context = super().get_context(request)
        s = get_search_backend()
        posts = s.search(word, BlogPage)
        #Page.objects.search("key", fields=["title"])
        context['posts'] = posts
        return context

class BlogTree(Page):
    def get_context(self, request):
        context = super().get_context(request)

        index = BlogIndexPage.objects.filter(title='Posts')[0]
        #posts = index.get_children().live()
        #print(posts)

        html_menu = PageTree(index).html_menu
        context['menu'] = html_menu
        setContext(context)

        return context

@register_snippet
class BlogCategory(models.Model):
    name = models.CharField(max_length=255)
    icon = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+'
    )

    panels = [
        FieldPanel('name'),
        ImageChooserPanel('icon'),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        
