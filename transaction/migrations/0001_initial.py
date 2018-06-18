# Generated by Django 2.0.4 on 2018-06-18 21:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('catalogue', '0011_create_products_instances'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('sale', 'Sale'), ('sample', 'Sample'), ('spoil', 'Spoil'), ('return', 'Return')], max_length=32)),
                ('retailer', models.CharField(choices=[('amazon', 'Amazon'), ('website', 'Website'), ('n/a', 'N/A')], max_length=32)),
                ('description', models.TextField(blank=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=9)),
                ('payment_type', models.CharField(choices=[('cash', 'Cash'), ('card', 'Card'), ('amazon', 'Amazon'), ('paypal', 'PayPal'), ('n/a', 'N/A')], max_length=32)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalogue.Product')),
            ],
        ),
    ]