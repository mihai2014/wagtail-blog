from django.db import models

from modelcluster.fields import ParentalKey
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

    def serve(self, request):
        #try:
        #    page_req = request.GET['page']
        #except:
        #    page_req = "first"

        current_page = int( request.COOKIES.get('myblog_page', '1') )

        #reset page cookie to 1
        if(len(request.GET)==0):
            current_page = 1

        index_blog = Page.objects.get(slug='index-blog')
        children = index_blog.get_children()
        for child in children:
            if(child.title=="Posts"):
                posts = child

        nr_posts = posts.get_children().live().count()
        intervals = pageLimits(nr_posts)
        max_page = len(intervals)   


        #print("current_page",current_page)
        interval = intervals[current_page-1]
        limit1 = interval[0]
        limit2 = interval[1]
        #print(limit1,limit2)

        blogpages = posts.get_children().live().order_by('-first_published_at')[limit1:limit2]
        #blogpages = self.get_children().live().order_by('-first_published_at')[limit1:limit2]

        template = get_template('blog/blog_index_page.html')
        context = super().get_context(request)
        context['blogpages'] = blogpages
        setContext(context)
        response = HttpResponse(template.render(context, request))

        if(current_page == 1): #or page_req == 'first':
            response.set_cookie('myblog_page', str(current_page), max_age=None)
            response.set_cookie('max_page', str(max_page), max_age=None)

        return(response)


#    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
#        context = super().get_context(request)
#        blogpages = self.get_children().live().order_by('-first_published_at') 
#        print(len(blogpages))
#        context['blogpages'] = blogpages
#        context['page'] = '1'
#        return context


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

    body = StreamField([
        ('heading', blocks.CharBlock(classname="full title")),
        ('paragraph', blocks.RichTextBlock()),
        ('two_columns', TwoColumnBlock()),
        ('three_columns', ThreeColumnBlock()),
        ('image_center', ImageCenterBlock()),
        ('image_left', ImageLeftBlock()),
        #('htmljs', blocks.TextBlock()),
        #('code_bash', blocks.TextBlock()),
        #('code_py', blocks.TextBlock()),
        #('code_htmljs', blocks.TextBlock()),
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

    
