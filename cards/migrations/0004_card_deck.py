# Generated by Django 4.2.2 on 2023-06-20 14:24

from django.db import migrations, models

def copy_box_to_deck(apps, schema_editor):
    Card = apps.get_model('cards', 'Card')
    for card in Card.objects.all():
        card.deck = card.box
        card.save()

class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0003_rename_correct_answers_card_knownanswercount_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='deck',
            field=models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], default=1),
        ),
        migrations.RunPython(copy_box_to_deck),
    ]
