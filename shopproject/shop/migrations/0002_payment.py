# Generated by Django 5.0.3 on 2024-03-24 09:07

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('type', models.CharField(choices=[('credit', 'Credit'), ('debit', 'Debit')], default='credit', max_length=6)),
                ('is_active', models.BooleanField(default=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('consumer', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='shop.consumer')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments_created', to=settings.AUTH_USER_MODEL)),
                ('shop', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='shop.shop')),
                ('updated_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments_updated', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
