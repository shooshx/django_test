# Generated by Django 2.0.10 on 2019-02-16 15:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog_test', '0002_codesnippet'),
    ]

    operations = [
        migrations.CreateModel(
            name='WarriorDef',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=80)),
                ('wtype', models.IntegerField()),
                ('code1', models.TextField()),
                ('code2', models.TextField()),
                ('update_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('owner_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='codesnippet',
            name='owner_user',
        ),
        migrations.DeleteModel(
            name='CodeSnippet',
        ),
    ]
