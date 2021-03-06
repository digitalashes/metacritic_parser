# Generated by Django 2.1.5 on 2019-02-06 10:24

import django.utils.timezone
import model_utils.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False,
                                                                verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False,
                                                                      verbose_name='modified')),
                ('title', models.CharField(help_text='Game name.', max_length=128, verbose_name='Title')),
                ('score', models.PositiveIntegerField(default=0, help_text='Game score.', verbose_name='Score')),
            ],
            options={
                'verbose_name': 'Game',
                'verbose_name_plural': 'Games',
                'ordering': ('title',),
            },
        ),
        migrations.CreateModel(
            name='Platform',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Platform name.', max_length=64, verbose_name='Platform')),
            ],
            options={
                'verbose_name': 'Platform',
                'verbose_name_plural': 'Platforms',
                'ordering': ('name',),
            },
        ),
        migrations.AddIndex(
            model_name='platform',
            index=models.Index(fields=['name'], name='metacritic__name_395318_idx'),
        ),
        migrations.AddField(
            model_name='game',
            name='platform',
            field=models.ForeignKey(help_text='Platform name.', on_delete=django.db.models.deletion.CASCADE,
                                    related_name='games', to='metacritic.Platform', verbose_name='Platform'),
        ),
        migrations.AddIndex(
            model_name='game',
            index=models.Index(fields=['platform', 'title', 'score', 'created'], name='metacritic__platfor_7a573f_idx'),
        ),
    ]
