# Generated by Django 4.2.3 on 2023-07-18 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogmain', '0006_alter_blog_content'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscriber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
            ],
        ),
    ]