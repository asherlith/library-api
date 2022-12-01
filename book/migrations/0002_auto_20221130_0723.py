# Generated by Django 3.2.16 on 2022-11-30 07:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='person_lent_to',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='book.person'),
        ),
        migrations.AlterField(
            model_name='book',
            name='return_date',
            field=models.DateTimeField(blank=True),
        ),
    ]
