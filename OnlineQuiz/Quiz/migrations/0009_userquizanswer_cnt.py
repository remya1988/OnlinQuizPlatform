# Generated by Django 4.0.6 on 2023-03-02 08:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Quiz', '0008_userquizanswer'),
    ]

    operations = [
        migrations.AddField(
            model_name='userquizanswer',
            name='cnt',
            field=models.PositiveBigIntegerField(default=1),
        ),
    ]