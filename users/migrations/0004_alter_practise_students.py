# Generated by Django 4.1.7 on 2023-03-20 21:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_practisesubmission'),
    ]

    operations = [
        migrations.AlterField(
            model_name='practise',
            name='students',
            field=models.ManyToManyField(blank=True, related_name='practises', to='users.student'),
        ),
    ]
