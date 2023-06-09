# Generated by Django 4.1.7 on 2023-05-10 08:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('RecipeManager', '0004_shoppinglist'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecipeReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review_text', models.TextField()),
                ('review_rating', models.IntegerField(default=0)),
                ('recipe_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='RecipeManager.recipeentry')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
