# Generated by Django 4.1.3 on 2022-11-16 19:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('cname', models.CharField(max_length=80)),
                ('email', models.EmailField(max_length=40, unique=True)),
                ('address', models.CharField(blank=True, max_length=200, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'db_table': 'Customer',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('cityid', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=50)),
                ('state', models.CharField(max_length=2)),
            ],
            options={
                'db_table': 'City',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Flight',
            fields=[
                ('fid', models.AutoField(primary_key=True, serialize=False)),
                ('fnumber', models.IntegerField(blank=True, null=True)),
                ('fdate', models.DateField()),
                ('ftime', models.TimeField()),
                ('price', models.FloatField()),
                ('class_field', models.IntegerField(db_column='class')),
                ('capacity', models.IntegerField()),
                ('available', models.IntegerField()),
                ('dest', models.ForeignKey(db_column='dest', on_delete=django.db.models.deletion.CASCADE, to='main.city')),
                ('orig', models.ForeignKey(db_column='orig', on_delete=django.db.models.deletion.CASCADE, related_name='cities', to='main.city')),
            ],
            options={
                'db_table': 'Flight',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('ordernum', models.AutoField(primary_key=True, serialize=False)),
                ('qty', models.IntegerField()),
                ('cardnum', models.CharField(max_length=16)),
                ('cardmonth', models.IntegerField()),
                ('cardyear', models.IntegerField()),
                ('order_date', models.DateField(blank=True, null=True)),
                ('cid', models.ForeignKey(db_column='cid', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('dfid', models.ForeignKey(db_column='dfid', on_delete=django.db.models.deletion.CASCADE, related_name='flights', to='main.flight')),
                ('rfid', models.ForeignKey(blank=True, db_column='rfid', null=True, on_delete=django.db.models.deletion.CASCADE, to='main.flight')),
            ],
            options={
                'db_table': 'Reservation',
                'managed': True,
            },
        ),
    ]
