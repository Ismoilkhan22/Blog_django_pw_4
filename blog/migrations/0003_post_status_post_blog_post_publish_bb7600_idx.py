# Generated by Django 5.1.1 on 2024-09-30 06:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_alter_post_options_post_created_post_publish_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='status',
            field=models.CharField(choices=[('DF', 'DRAFT'), ('PB', 'Published')], default='DF', max_length=2),
        ),
        migrations.AddIndex(
            model_name='post',
            index=models.Index(fields=['-publish'], name='blog_post_publish_bb7600_idx'),
        ),
    ]
