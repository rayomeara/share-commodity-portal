# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2020-03-20 18:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('listing', '0002_commodity_unit'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=50)),
                ('phone_number', models.CharField(max_length=20)),
                ('postcode', models.CharField(blank=True, max_length=20)),
                ('town_or_city', models.CharField(max_length=40)),
                ('street_address1', models.CharField(max_length=40)),
                ('street_address2', models.CharField(max_length=40)),
                ('country', models.CharField(max_length=40)),
                ('date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='PaymentCommodityItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('commodity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='listing.Commodity')),
                ('payment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='payment.Payment')),
            ],
        ),
        migrations.CreateModel(
            name='PaymentShareItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('payment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='payment.Payment')),
                ('share', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='listing.Share')),
            ],
        ),
    ]
