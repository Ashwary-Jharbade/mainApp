# Generated by Django 3.0.4 on 2020-03-29 05:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mainApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserDeatils',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fullname', models.CharField(max_length=50)),
                ('gender', models.CharField(max_length=10)),
                ('dateofbirth', models.DateField()),
                ('occupation', models.CharField(max_length=30)),
                ('maritialstatus', models.CharField(max_length=10)),
                ('mobile', models.CharField(max_length=10)),
                ('laddress', models.CharField(max_length=100)),
                ('paddress', models.CharField(max_length=100)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]