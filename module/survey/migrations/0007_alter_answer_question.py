# Generated by Django 3.2.4 on 2021-07-01 11:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0006_answer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(blank=True, help_text='Chọn khảo sát', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='answer', to='survey.question'),
        ),
    ]
