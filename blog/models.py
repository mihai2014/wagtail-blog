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

# Create your models here.

#def set_cookie(response, key, value, days_expire = 7):
#    if days_expire is None:
#        max_age = 365 * 24 * 60 * 60  #one year
#    else:
#        max_age = days_expire * 24 * 60 * 60 
#    expires = datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age), "%a, %d-%b-%Y %H:%M:%S GMT")
#    response.set_cookie(key, value, max_age=max_age, expires=expires, domain=settings.SESSION_COOKIE_DOMAIN, secure=settings.SESSION_COOKIE_SECURE or None


class BlogIndexPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full")
    ]

    def serve(self, request):
        #'next' / 'prev'
        try:
            page_req = request.GET['page']
        except:
            page_req = "first"

        current_page = int( request.COOKIES.get('myblog_page', '0') )

        #print('page',current_page)
        print(page_req)

        context = super().get_context(request)
        blogpages = self.get_children().live().order_by('-first_published_at')

        max_page = 10;

        context['blogpages'] = blogpages
        template = get_template('blog/blog_index_page.html')
        response = HttpResponse(template.render(context, request))

        if(current_page == 0): #or page_req == 'first':
            current_page = 1
            response.set_cookie('myblog_page', str(current_page), max_age=None)
            response.set_cookie('max_page', str(max_page), max_age=None)

#        else:
#            if page_req == 'next':
#                if current_page < total_pages:
#                    current_page += 1
#                    response.set_cookie('myblog_page', str(current_page), max_age=None)
#            if page_req == 'prev':   
#                if current_page > 1:
#                    current_page -= 1
#                    response.set_cookie('myblog_page', str(current_page), max_age=None)

#        print('page',current_page)

        return(response)


#    def get_context(self, request):

        # Update context to include only published posts, ordered by reverse-chron
#        context = super().get_context(request)
#        blogpages = self.get_children().live().order_by('-first_published_at')  #[0:len(blogpages)]
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
    body = RichTextField(blank=True)
    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)

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
        MultiFieldPanel([
            FieldPanel('date'),
            FieldPanel('tags'),
        ], heading="Blog information"),
        FieldPanel('intro'),
        FieldPanel('body'),
        InlinePanel('gallery_images', label="Gallery images"),
    ]


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


