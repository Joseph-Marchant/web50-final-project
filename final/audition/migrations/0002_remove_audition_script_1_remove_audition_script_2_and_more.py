# Generated by Django 4.0.3 on 2022-03-29 08:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('audition', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='audition',
            name='script_1',
        ),
        migrations.RemoveField(
            model_name='audition',
            name='script_2',
        ),
        migrations.RemoveField(
            model_name='audition',
            name='script_3',
        ),
        migrations.RemoveField(
            model_name='audition',
            name='script_4',
        ),
        migrations.RemoveField(
            model_name='audition',
            name='script_5',
        ),
        migrations.CreateModel(
            name='Script',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('scene', models.CharField(max_length=64)),
                ('script', models.CharField(max_length=1000)),
                ('audition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scenes', to='audition.audition')),
            ],
        ),
    ]
