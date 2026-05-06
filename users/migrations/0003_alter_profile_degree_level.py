from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='degree_level',
            field=models.CharField(
                blank=True,
                choices=[
                    ('hsc', 'HSC'),
                    ('bachelor', "Bachelor's"),
                    ('master', "Master's"),
                    ('phd', 'PhD'),
                ],
                max_length=50,
                null=True,
            ),
        ),
    ]