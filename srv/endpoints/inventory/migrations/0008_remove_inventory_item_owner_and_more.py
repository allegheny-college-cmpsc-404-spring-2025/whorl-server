# Generated by Django 5.0.6 on 2024-06-10 23:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0007_alter_inventory_item_owner'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inventory',
            name='item_owner',
        ),
        migrations.AlterField(
            model_name='inventory',
            name='item_name',
            field=models.CharField(max_length=225, unique=True),
        ),
    ]
