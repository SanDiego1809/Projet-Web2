# Generated by Django 3.2.8 on 2021-11-28 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_post_sell_rent'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='place',
            field=models.CharField(default='Bruxelles', max_length=100),
        ),
        migrations.AlterField(
            model_name='post',
            name='sell_rent',
            field=models.CharField(choices=[('S', 'To Sell'), ('R', 'To Rent')], default='S', max_length=10),
        ),
    ]
