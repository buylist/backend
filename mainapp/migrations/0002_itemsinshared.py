# Generated by Django 2.2.1 on 2019-07-21 07:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ItemsInShared',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.DecimalField(decimal_places=4, max_digits=12)),
                ('unit', models.TextField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('deleted', models.NullBooleanField()),
                ('value', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=8, verbose_name='стоимость выбранного количества')),
                ('checklist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.Checklist')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.Item')),
            ],
        ),
    ]
