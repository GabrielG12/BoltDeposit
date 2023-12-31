# Generated by Django 5.0 on 2023-12-06 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bank_accounts', '0002_bankaccount_delete_balance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bankaccount',
            name='balance',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='bankaccount',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
