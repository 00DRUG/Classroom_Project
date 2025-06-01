from django.db import migrations

def create_general_subject(apps, schema_editor):
    Subject = apps.get_model('polls', 'Subject')
    # Check if "General" subject already exists (optional)
    if not Subject.objects.filter(name='General').exists():
        Subject.objects.create(name='General')
class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0010_subject'),
    ]

    operations = [
        migrations.RunPython(create_general_subject),
    ]
