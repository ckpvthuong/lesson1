# Generated by Django 3.2.4 on 2021-07-01 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0003_auto_20210701_1127'),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(blank=True, help_text='Hãy điền câu hỏi ở đây!', max_length=255, null=True)),
            ],
            options={
                'verbose_name': 'Câu hỏi',
                'verbose_name_plural': 'Câu hỏi',
                'db_table': 'tbl_question',
            },
        ),
        migrations.AlterModelOptions(
            name='survey',
            options={'verbose_name': 'Survey', 'verbose_name_plural': 'Danh sách khảo sát'},
        ),
    ]
