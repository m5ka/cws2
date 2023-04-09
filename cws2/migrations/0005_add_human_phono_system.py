
import shortuuid
import json
from django.db import migrations


def add_human_phono_system(apps, schema_editor):
    User = apps.get_model("cws2", "User")
    PhonoSystem = apps.get_model("cws2", "PhonoSystem")
    Phone = apps.get_model("cws2", "Phone")
    sheep_user = User.objects.filter(username="sheep")[0]
    human_phono_system = PhonoSystem.objects.create(
        uuid=shortuuid.uuid(),
        is_public=True,
        is_shared=False,
        is_human=True,
        name="Human Phono System",
        status="P",
        description="IPA phono system which represents human speech.",
        created_by=sheep_user,
        owned_by=sheep_user,
    )
    json_file = open('./data/human_phono_system.json')
    json_data = json.load(json_file)
    json_file.close
    for phone_data in json_data['phones']:
        Phone.objects.create(
            uuid=shortuuid.uuid(),
            phono_system=human_phono_system,
            glyph=phone_data['glyph'],
            name=phone_data['name'],
            category=phone_data['category'][0:1],
            ipa=phone_data['ipa'] if 'ipa' in phone_data else None,
            xsampa=phone_data['xsampa'] if 'xsampa' in phone_data else None,
            tags=phone_data['tags'],
            created_by=sheep_user,
        )


class Migration(migrations.Migration):
    dependencies = [
        ("cws2", "0004_phono_systems"),
    ]

    operations = [
        migrations.RunPython(add_human_phono_system,
                             reverse_code=migrations.RunPython.noop),
    ]
