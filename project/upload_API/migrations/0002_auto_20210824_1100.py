# Generated by Django 3.2.6 on 2021-08-24 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upload_API', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlockItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current_block', models.PositiveIntegerField()),
                ('begin_row', models.PositiveIntegerField()),
                ('end_row', models.PositiveIntegerField()),
                ('begin_col', models.PositiveIntegerField()),
                ('end_col', models.PositiveIntegerField()),
            ],
        ),
        migrations.DeleteModel(
            name='BlockItems',
        ),
    ]
