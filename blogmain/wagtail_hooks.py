from wagtail.contrib.modeladmin.options import (
    ModelAdmin, modeladmin_register,
)
from .models import Comment

class CommentAdmin(ModelAdmin):
    model = Comment
    menu_icon = 'comment'
    menu_label = 'Comments'
    menu_order = 200
    add_to_settings_menu = False
    list_display = ('username','comment')
    search_fields = ('username','comment')


modeladmin_register(CommentAdmin)