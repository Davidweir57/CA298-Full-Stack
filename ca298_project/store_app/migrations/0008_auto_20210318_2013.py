# Generated by Django 3.1.6 on 2021-03-18 20:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store_app', '0007_product_subcategory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
