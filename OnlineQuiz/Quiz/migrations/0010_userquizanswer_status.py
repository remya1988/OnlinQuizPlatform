# Generated by Django 4.0.6 on 2023-03-02 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Quiz', '0009_userquizanswer_cnt'),
    ]

    operations = [
        migrations.AddField(
            model_name='userquizanswer',
            name='status',
            field=models.CharField(default='Failed', max_length=20),
        ),
    ]
