# Generated by Django 3.0.4 on 2020-04-07 09:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0008_actionlist_actdate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='actionlist',
            name='police',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainApp.PoliceDetail'),
        ),
    ]