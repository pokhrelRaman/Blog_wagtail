# Generated by Django 4.2.3 on 2023-07-08 07:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogmain', '0003_blogspage_testcontent_delete_blogpage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='testcontent',
            name='approved',
        ),
        migrations.RemoveField(
            model_name='testcontent',
            name='firstName',
        ),
        migrations.RemoveField(
            model_name='testcontent',
            name='lastName',
        ),
        migrations.AddField(
            model_name='testcontent',
            name='content',
            field=models.CharField(default='no title', max_length=300),
        ),
        migrations.AlterField(
            model_name='testcontent',
            name='title',
            field=models.CharField(default='no title', max_length=20),
        ),
    ]
