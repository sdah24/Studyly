from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('universities', '0004_alter_program_level'),
    ]

    operations = [
        migrations.AddField(
            model_name='university',
            name='apply_url',
            field=models.URLField(blank=True, null=True, help_text='Direct application portal URL'),
        ),
    ]