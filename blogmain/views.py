# models and serializer
from .models import BlogsPage,Comment
from user.models import User
from .serializer import BlogPageSerializer,BlogPageAndCommentSerializer,CommentSerializer

# imports from rest_framework
from rest_framework import status
from rest_framework.response import Response 
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.generics import RetrieveAPIView,CreateAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from customlib.views.views import PutAPIView 

#for Swagger
from drf_yasg.utils import swagger_auto_schema
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


# Create your views here.

class BlogView(RetrieveAPIView):
    
    permission_classes = [AllowAny]
    serializer_class = BlogPageSerializer
    
    @swagger_auto_schema(
        responses={204: "No Content"},
    )
    @method_decorator(csrf_exempt)
    def get(self,request):
        blogs = BlogsPage.objects.live()
        print(blogs)
        blog = BlogPageSerializer(blogs,many=True)
        print(blog.data)
        return Response(blog.data)
        # serializer = BlogSerializer(blog,many=True)

class BlogAndCommentView(RetrieveAPIView):

    permission_classes = [AllowAny]
    serializer_class = BlogPageAndCommentSerializer
    
    @swagger_auto_schema(
        responses={204: "No Content"},
    )
    @method_decorator(csrf_exempt)

    def get(self,request,blogID):
        blog = BlogsPage.objects.live().get(id = blogID)
        blog = BlogPageAndCommentSerializer(blog)
        return Response(blog.data)

class CreateCommentView(CreateAPIView):
   
    permission_class = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = CommentSerializer

    @swagger_auto_schema(
        request_body = CommentSerializer,
        responses={204: "No Content"},
    )
    @method_decorator(csrf_exempt)

    def post(self,request):
        user = request.user
        username = user.username
        if user.is_authenticated:
            print(username,"username yeri ho ")
            serializer = CommentSerializer(data= request.data,context= {'username': username})
            if serializer.is_valid():
                serializer.save()
                return Response({'msg':'comment has been posted'})
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        return Response({'msg':'Unauthorised user cannot post'})

class UpdateCommentView(PutAPIView):
    authentication_classes = [JWTAuthentication]
    permission_class = [IsAuthenticated]
    serializer_class = CommentSerializer
    
    @swagger_auto_schema(
        request_body = CommentSerializer,
        responses={204: "No Content"},
    )
    @method_decorator(csrf_exempt)    
    
    def put(self,request,commentID):
        user = request.user
        comment = Comment.objects.get(id = commentID)
        print(user.username)
        if comment.username != user.username:
            return Response({'msg':'You cannot modify this content'})
        
        serializer = CommentSerializer(instance= comment,data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'comment has been updated'})
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
