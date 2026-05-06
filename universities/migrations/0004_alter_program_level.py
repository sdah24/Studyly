from django.db import migrations, models


def remap_levels_forward(apps, schema_editor):
    Program = apps.get_model('universities', 'Program')
    mapping = {
        'bachelor': 'bsc',
        'master': 'msc',
        # 'phd' and 'mba' are unchanged
    }
    for old, new in mapping.items():
        Program.objects.filter(level=old).update(level=new)


def remap_levels_backward(apps, schema_editor):
    Program = apps.get_model('universities', 'Program')
    mapping = {
        'bsc': 'bachelor',
        'msc': 'master',
    }
    for old, new in mapping.items():
        Program.objects.filter(level=old).update(level=new)


class Migration(migrations.Migration):

    dependencies = [
        ('universities', '0003_university_image'),
    ]

    operations = [
        migrations.RunPython(remap_levels_forward, remap_levels_backward),
        migrations.AlterField(
            model_name='program',
            name='level',
            field=models.CharField(
                choices=[
                    ('bsc', 'BSc'),
                    ('msc', 'MSc'),
                    ('mba', 'MBA'),
                    ('phd', 'PhD'),
                    ('diploma', 'Diploma'),
                    ('certificate', 'Certificate'),
                ],
                default='msc',
                max_length=20,
            ),
        ),
    ]