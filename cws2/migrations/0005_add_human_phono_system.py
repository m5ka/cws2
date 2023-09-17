import json

import shortuuid
from django.db import migrations
from pathlib import Path


def add_human_phono_system(apps, schema_editor):
    User = apps.get_model("cws2", "User")
    PhonoSystem = apps.get_model("cws2", "PhonoSystem")
    Phone = apps.get_model("cws2", "Phone")
    sheep = User.objects.get(username="sheep")
    human_phono_system = PhonoSystem.objects.create(
        uuid=shortuuid.uuid(),
        is_public=True,
        is_shared=False,
        is_human=True,
        name="Human Phono System",
        status="P",
        description="IPA phono system which represents human speech.",
        created_by=sheep,
        owned_by=sheep,
    )
    json_file_location = (
        Path(__file__).resolve(strict=True).parent / "data" / "human_phono_system.json"
    )
    json_file = open(json_file_location)
    json_data = json.load(json_file)
    json_file.close()
    for phone_data in json_data["phones"]:
        Phone.objects.create(
            uuid=shortuuid.uuid(),
            phono_system=human_phono_system,
            glyph=phone_data["glyph"],
            name=phone_data["name"],
            category=phone_data["category"][0:1],
            ipa=phone_data["ipa"] if "ipa" in phone_data else None,
            xsampa=phone_data["xsampa"] if "xsampa" in phone_data else "",
            tags=phone_data["tags"],
            created_by=sheep,
        )


class Migration(migrations.Migration):
    dependencies = [
        ("cws2", "0004_phono_system_phone"),
    ]

    operations = [
        migrations.RunPython(
            add_human_phono_system, reverse_code=migrations.RunPython.noop
        ),
    ]
