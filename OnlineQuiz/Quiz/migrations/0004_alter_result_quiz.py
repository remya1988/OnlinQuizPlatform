# Generated by Django 4.0.6 on 2023-02-24 12:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Quiz', '0003_category_questions_date_questions_difficulty_level_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='result',
            name='quiz',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Quiz.questions'),
        ),
    ]