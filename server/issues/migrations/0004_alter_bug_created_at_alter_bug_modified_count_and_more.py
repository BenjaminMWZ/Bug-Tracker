# Generated by Django 4.2.20 on 2025-04-07 00:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('issues', '0003_delete_bugmodification'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bug',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='bug',
            name='modified_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='bug',
            name='priority',
            field=models.CharField(choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')], default='medium', max_length=10),
        ),
        migrations.AlterField(
            model_name='bug',
            name='status',
            field=models.CharField(choices=[('open', 'Open'), ('in_progress', 'In Progress'), ('resolved', 'Resolved'), ('closed', 'Closed')], default='open', max_length=20),
        ),
        migrations.AlterField(
            model_name='bug',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
