# Generated by Django 3.1.7 on 2021-03-22 02:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boardapp', '0003_auto_20210316_1508'),
    ]

    operations = [
        migrations.CreateModel(
            name='Boardreply',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('boardId', models.CharField(max_length=256)),
                ('writer', models.CharField(max_length=256)),
                ('content', models.TextField()),
                ('regdate', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'boardreply',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=256)),
                ('userpassword', models.CharField(max_length=256)),
                ('usermail', models.TextField()),
                ('regDate', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'user',
                'managed': False,
            },
        ),
    ]
