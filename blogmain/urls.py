from django.urls import path
from .views  import BlogView,BlogAndCommentView,CreateCommentView,UpdateCommentView


urlpatterns = [
    path('allBlog',BlogView.as_view()),
    path('blog/<int:blogID>',BlogAndCommentView.as_view()),
    path('comment',CreateCommentView.as_view()),
    path('comment/<int:commentID>',UpdateCommentView.as_view()),
] 