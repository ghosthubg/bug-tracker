# Generated by Django 4.2.4 on 2023-09-21 17:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bug',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('status', models.CharField(choices=[('new', 'New'), ('fixed', 'Fixed'), ('under_review', 'Under Review')], default='new', max_length=20)),
                ('severity', models.CharField(choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')], default='low', max_length=20)),
                ('screenshot', models.ImageField(blank=True, null=True, upload_to='bug_screenshots/')),
                ('steps_to_reproduce', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Developer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='ChangeStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('new', 'New'), ('fixed', 'Fixed'), ('under_review', 'Under Review')], max_length=20)),
                ('comment', models.TextField()),
                ('change_time', models.DateTimeField(auto_now_add=True)),
                ('bug', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='network.bug')),
            ],
        ),
        migrations.CreateModel(
            name='BugComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('comment_time', models.DateTimeField(auto_now_add=True)),
                ('commenter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='bug',
            name='comments',
            field=models.ManyToManyField(blank=True, related_name='bug_comments', to='network.bugcomment'),
        ),
        migrations.AddField(
            model_name='bug',
            name='reporter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='AssignedDeveloper',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_assigned', models.DateField()),
                ('bug', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='network.bug')),
                ('developer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='network.developer')),
            ],
        ),
    ]
