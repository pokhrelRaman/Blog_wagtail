from wagtail.admin.panels import (
    InlinePanel,
    FieldPanel,
    FieldRowPanel,
    MultiFieldPanel
)
from django.db import models
from wagtail.models import Page
from wagtail.models import Comment
from wagtail.api import APIField
from wagtail.models import Orderable
from wagtail.fields import RichTextField

from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel

from taggit.models import TaggedItemBase
from modelcluster.contrib.taggit import ClusterTaggableManager

from wagtail.search import index

def upload_to(instance,filename):
    return 'blog/thumbnail/images{filename}'.format(filename=filename)


# @route(r'^search/$')

class BlogTag(TaggedItemBase):
    content_object = ParentalKey('Blog', related_name='blog_tag', on_delete=models.CASCADE)


class BlogsPage(Page):
    content_panels = Page.content_panels + [
        InlinePanel('blog', label= 'New Blog'),
    ]

class Blog(Orderable,ClusterableModel):
    page = ParentalKey('BlogsPage', on_delete=models.CASCADE,
                       related_name='blog', null=True)
    author = models.CharField(null=True,max_length=20)
    content = RichTextField(null=True,max_length=2000)
    category = models.CharField(max_length=20,blank=True,null=False)
    tags = ClusterTaggableManager(through= BlogTag, blank=True)
    thumbnail = models.ImageField(upload_to= upload_to, null = True, default= "") 
    

    api_fields = [
        APIField('author'),
        APIField('content'),
        APIField('category'),
        APIField('tags'),
        APIField('thumbnail'),
    ]

    # search_fields = Page.search_fields + [
    #     index.SearchField('author'),
    #     index.SearchField('category'),
    #     index.SearchField('tags'),
    # ]

    search_fields = [
        index.SearchField('author',  AutocompleteField=True),
        index.SearchField('category',  AutocompleteField=True),
        index.SearchField('tags',  AutocompleteField=True),
        index.SearchField('content', AutocompleteField=True),
    ]


    def __str__(self):
        return self.author





class Comment(models.Model):
    
    username = models.CharField(max_length=20, default = "anonymous")
    comment = models.CharField(max_length=200,default = "")
    blog = models.ForeignKey(BlogsPage,on_delete=models.CASCADE,blank=True,null= False)

    panels = [
        FieldPanel('username'),
        FieldPanel('comment'),
        FieldPanel('blog'),
    ]

    api_fields = [
        APIField('username'),
        APIField('comment'),
        APIField('blog'),
    ]


    def __str__(self):
        return self.username