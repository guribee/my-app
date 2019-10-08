# Generated by Django 2.2.4 on 2019-10-05 01:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_auto_20191005_0059'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rateplan',
            name='loan_company',
            field=models.CharField(choices=[('一括', '一括'), ('PFクレジット', 'PFクレジット'), ('アプラス①', 'アプラス①'), ('アプラス②', 'アプラス②'), ('アプラス③', 'アプラス③'), ('PFS', 'PFS'), ('FLEX', 'FLEX'), ('セディナ', 'セディナ'), ('西京カード', '西京カード'), ('シティックス', 'シティックス')], default='アプラス①', max_length=10, verbose_name='支払方法'),
        ),
    ]