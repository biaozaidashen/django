# Generated by Django 2.0.5 on 2018-05-22 02:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dept',
            fields=[
                ('dno', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
                ('location', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Emp',
            fields=[
                ('no', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
                ('job', models.CharField(max_length=10)),
                ('sal', models.DecimalField(decimal_places=2, max_digits=7)),
                ('comm', models.DecimalField(decimal_places=2, max_digits=7, null=True)),
                ('dept', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='hrs.Dept')),
            ],
        ),
    ]
