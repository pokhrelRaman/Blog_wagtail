# Generated by Django 4.2.3 on 2023-07-22 09:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blogmain', '0012_rename_blogid_comment_blog'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='blog',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='blogmain.blogspage'),
        ),
    ]
