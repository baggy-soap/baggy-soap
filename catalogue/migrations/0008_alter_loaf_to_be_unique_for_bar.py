# Generated by Django 2.0.4 on 2018-06-11 21:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0007_add_image_to_soap_bar_and_baggy_soap'),
    ]

    operations = [
        migrations.AlterField(
            model_name='soapbar',
            name='loaf',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='catalogue.SoapLoaf'),
        ),
    ]
