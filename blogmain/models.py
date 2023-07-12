from wagtail.admin.panels import (
    InlinePanel,
    FieldPanel,
    FieldRowPanel,
    MultiFieldPanel
)
from django.db import models
from wagtail.models import Page
from wagtail.api import APIField
from wagtail.models import Orderable
from wagtail.fields import RichTextField
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel




class BlogsPage(Page):
    # max_count = 1
    content_panels = Page.content_panels + [
        InlinePanel('blog', label= 'New Blog'),
        InlinePanel('comment', label= 'Comment')
    ]

class Blog(Orderable):
    max_count = 1 
    page = ParentalKey('BlogsPage', on_delete=models.CASCADE,
                       related_name='blog', null=True)
    author = models.CharField(null=True,max_length=20)
    content = RichTextField(null=True,max_length=2000)

    api_fields = [
        APIField('author'),
        APIField('content'),
    ]


class Comment(ClusterableModel):
    page = ParentalKey('BlogsPage', on_delete=models.CASCADE,
                       related_name='comment', null=True)

    username = models.CharField(max_length=20, default = "anonymous")
    comment = models.CharField(max_length=300,default = "")

    panels = [
        FieldPanel('username'),
        FieldPanel('comment')
    ]

    api_fields = [
        APIField('username'),
        APIField('comment'),
    ]

    def __str__(self):
        return self.username