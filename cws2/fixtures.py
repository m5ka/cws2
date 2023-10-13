import random
import sys

from faker import Faker
from slugify.slugify import slugify

from cws2.constants import GroupAccessType, LanguageStatus, LanguageType
from cws2.models.group import Group
from cws2.models.language import Dialect, Language
from cws2.models.user import User


class Fixtures:
    email_providers = [
        "gmail.com",
        "outlook.com",
        "hotmail.com",
        "aol.com",
        "proton.me",
    ]
    language_name_suffixes = ["ish", "ian", "ese", "ic"]

    def __init__(self, stdout=sys.stdout):
        self.fake = Faker("en_GB")
        self.stdout = stdout
        self.users = []

    def chance(self, i):
        return bool(random.randint(0, 99) < i)

    def chance_or_blank(self, value, chance=50):
        if self.chance(chance):
            return value
        return ""

    def create_username(self, name):
        if self.chance(50):
            name = name.lower().replace(" ", ".")
        else:
            n = name.lower().split(" ")
            name = f"{n[0][:1]}{n[1]}"
        if self.chance(20):
            name += str(random.randint(11, 99))
        return name

    def create_email(self, name):
        return f"{self.create_username(name)}@{random.choice(self.email_providers)}"

    def create_user(self):
        name = self.fake.name()
        return User.objects.create_user(
            username=self.create_username(name),
            email=self.create_email(name),
            email_confirmed_at=self.fake.past_datetime(),
        )

    def create_language_name(self):
        return self.fake.word().title() + random.choice(self.language_name_suffixes)

    def create_language_code(self):
        return "".join(
            [
                self.fake.random_uppercase_letter()
                for _ in range(1, random.randint(3, 4))
            ]
        )

    def create_language(self, user=None):
        if not user:
            raise Exception("A language cannot be created without providing a user.")
        name = self.create_language_name()
        return Language.objects.create(
            created_by=user,
            owned_by=user,
            is_public=self.chance(80),
            name=name,
            slug=slugify(name),
            endonym=self.chance_or_blank(self.fake.word().title(), 60),
            description=self.chance_or_blank(self.fake.paragraph(), 60),
            language_type=random.choice(LanguageType.CHOICES),
            language_status=random.choice(LanguageStatus.CHOICES),
            code=self.chance_or_blank(self.create_language_code(), 30),
        )

    def create_dialect(self, language=None):
        if not language:
            raise Exception(
                "A dialect cannot be created without providing a parent language."
            )
        name = self.create_language_name()
        return Dialect.objects.create(
            created_by=language.created_by,
            owned_by=language.owned_by,
            is_public=self.chance(80),
            name=name,
            slug=slugify(name),
            endonym=self.chance_or_blank(self.fake.word().title(), 60),
            description=self.chance_or_blank(self.fake.paragraph(), 60),
        )

    def create_group(self, owner=None):
        if not owner:
            raise Exception("A group cannot be created without providing an owner.")
        name = self.fake.words()
        return Group.objects.create(
            name=name,
            slug=slugify(name),
            description=self.fake.paragraph(),
            icon=self.fake.emoji(),
            icon_colour_bg=self.fake.color().upper(),
            icon_colour_fg=self.fake.color().upper(),
            access_type=random.choice(GroupAccessType.CHOICES_PICKABLE),
        )

    def create_fixtures(self):
        for _ in range(1, 30):
            user = self.create_user()
            self.stdout.write(f"<User: {user.username}>\n")
            self.users.append(user)
            for _ in range(1, random.randint(1, 4)):
                language = self.create_language(user=user)
                self.stdout.write(f"\t<Language: {language.name}>\n")
                if self.chance(30):
                    for _ in range(1, random.randint(1, 3)):
                        dialect = self.create_dialect(language=language)
                        self.stdout.write(f"\t\t<Dialect: {dialect.name}>\n")
        for _ in range(1, 10):
            group = self.create_group(owner=random.choice(self.users))
            self.stdout.write(f"<Group: {group.name}>\n")
            chance = random.randint(1, 90)
            for user in self.users:
                if self.chance(chance):
                    group.add_user(user)
                    self.stdout.write(f"\t<GroupMembership: {user.username}>\n")
