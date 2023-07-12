from rest_framework  import serializers
from .models import BlogsPage,Comment,Blog



class CommentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Comment
        fields = '__all__'
    
    def create(self,data):
        print(self.context.get('username'))
        comment = Comment.objects.create(page = data['page'], comment = data.get('comment'), username = self.context.get('username'))
        return comment

    def update(self, instance, data):
        comment = data.get('comment')
        instance.comment = comment
        instance.save()
        return instance

class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model =  Blog
        fields = ['author','content','page','id']

class BlogPageSerializer(serializers.ModelSerializer):
    blog = BlogSerializer(many=True)
    class Meta:
        model = BlogsPage
        fields = ['blog','id']

class BlogPageAndCommentSerializer(serializers.ModelSerializer):
    blog = BlogSerializer(many=True)
    comment = CommentSerializer(many=True)
    class Meta:
        model = BlogsPage
        fields = ['blog','comment']

