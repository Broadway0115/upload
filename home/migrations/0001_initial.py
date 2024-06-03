# Generated by Django 4.2.13 on 2024-05-24 05:09

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Email_Record',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.TextField()),
                ('host', models.TextField()),
                ('to', models.TextField()),
                ('email_template', models.TextField()),
                ('create_time', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'email_record',
            },
        ),
        migrations.CreateModel(
            name='Members',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account', models.CharField(max_length=30)),
                ('password', models.CharField(max_length=30)),
                ('useremail', models.EmailField(max_length=30)),
                ('gender', models.CharField(max_length=5)),
                ('userbirth', models.DateField()),
                ('career', models.CharField(max_length=10)),
                ('resident', models.CharField(max_length=5)),
                ('received_mail', models.CharField(max_length=5)),
            ],
            options={
                'db_table': 'members',
            },
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('label', models.SlugField(unique=True)),
            ],
            options={
                'db_table': 'chat_room',
            },
        ),
        migrations.CreateModel(
            name='Survey_Outcome',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account', models.CharField(max_length=30)),
                ('Question1', models.CharField(max_length=20)),
                ('Question2', models.CharField(max_length=20)),
                ('Question3', models.CharField(max_length=20)),
                ('Question4', models.CharField(max_length=20)),
                ('Question5', models.CharField(max_length=20)),
                ('Question6', models.CharField(max_length=20)),
                ('Question7', models.CharField(max_length=200)),
            ],
            options={
                'db_table': 'survey_outcome',
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('handle', models.TextField()),
                ('message', models.TextField()),
                ('timestamp', models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='home.room')),
            ],
            options={
                'db_table': 'chat_message',
            },
        ),
    ]