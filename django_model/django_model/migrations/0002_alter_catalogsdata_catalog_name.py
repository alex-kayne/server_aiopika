# Generated by Django 4.0 on 2022-01-10 07:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_model', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='catalogsdata',
            name='catalog_name',
            field=models.TextField(db_index=True, null=True),
        ),
    ]
