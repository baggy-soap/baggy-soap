# Generated by Django 2.0.4 on 2018-06-20 20:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('catalogue', '0001_initial'),
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
            ],
        ),
        migrations.CreateModel(
            name='TransactionItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=9)),
                ('quantity', models.PositiveIntegerField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalogue.Product')),
                ('transaction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='transaction.Transaction')),
            ],
        ),
    ]
