# Generated by Django 4.2.6 on 2023-10-24 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='companydetails',
            name='logo',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]
