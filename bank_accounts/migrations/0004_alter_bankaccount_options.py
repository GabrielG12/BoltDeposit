# Generated by Django 5.0 on 2023-12-06 14:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bank_accounts', '0003_alter_bankaccount_balance_alter_bankaccount_id'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bankaccount',
            options={'verbose_name': 'Bank Account'},
        ),
    ]