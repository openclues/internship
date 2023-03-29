# Generated by Django 4.1.7 on 2023-03-20 21:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CareerCenter',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Coordinator',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Practise',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=150, null=True)),
                ('description', models.TextField(blank=True, max_length=500, null=True)),
                ('form', models.FileField(blank=True, null=True, upload_to='files')),
                ('due_Time', models.DateTimeField(blank=True, null=True)),
                ('coordinator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.coordinator')),
                ('students', models.ManyToManyField(related_name='practises', to='users.student')),
            ],
        ),
    ]
