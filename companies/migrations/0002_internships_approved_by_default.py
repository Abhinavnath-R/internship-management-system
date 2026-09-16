from django.db import migrations, models


def approve_all_internships(apps, schema_editor):
    """Approve every existing internship so no posting waits on admin approval."""
    Internship = apps.get_model('companies', 'Internship')
    Internship.objects.update(is_approved=True)


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='internship',
            name='is_approved',
            field=models.BooleanField(default=True, help_text='Internships go live immediately when posted'),
        ),
        migrations.RunPython(approve_all_internships, migrations.RunPython.noop),
    ]
