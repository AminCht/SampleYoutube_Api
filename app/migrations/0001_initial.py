# Generated by Django 4.1 on 2022-09-01 09:35

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AppUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('birth_date', models.DateField(null=True)),
                ('phone_number', models.CharField(max_length=255)),
                ('MEMBERSHIP_STATUS', models.CharField(choices=[('N', 'Normal'), ('P', 'Premium')], default='N', max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Subscriber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subscribe', models.PositiveIntegerField()),
                ('app_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.appuser')),
            ],
        ),
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='app/contents', validators=[django.core.validators.FileExtensionValidator(allowed_extensions='mp4')])),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('upload_date', models.DateTimeField(auto_now=True)),
                ('app_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.appuser')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('content', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.content')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.appuser')),
            ],
        ),
    ]
