from rest_framework  import serializers
from .models import BlogsPage,Comment,Blog
from taggit.models import Tag


class PostCommentSerializer(serializers.ModelSerializer):
    # swagger ko lagi matra serializer
    class Meta:
        model = Comment
        fields = '__all__'
    
    def create(self,data):
        print(self.context.get('username'))
        comment = Comment.objects.create(blog = self.context.get('blog'), comment = data.get('comment'), username = self.context.get('username'))
        return comment

    def update(self, instance, data):
        comment = data.get('comment')
        instance.comment = comment
        instance.save()
        return instance

class GetCommentSerializer(serializers.ModelSerializer): 
    class Meta:
        model = Comment
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['name']


class BlogSerializer(serializers.ModelSerializer):
    thumbnail = serializers.ImageField()
    tags = TagSerializer(many=True)
    class Meta:
        model =  Blog
        fields = ['author','content','page','id','thumbnail','tags','category']

class BlogPageSerializer(serializers.ModelSerializer):
    blog = BlogSerializer(many=True)
    class Meta:
        model = BlogsPage
        fields = ['blog','id','title'] 