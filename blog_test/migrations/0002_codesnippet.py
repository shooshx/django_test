# Generated by Django 2.0.10 on 2019-02-15 21:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog_test', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CodeSnippet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=80)),
                ('code', models.TextField()),
                ('update_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('owner_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
