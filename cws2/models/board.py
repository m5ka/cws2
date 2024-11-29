from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

from cws2.models.base import AutoSlugMixin, TransientModel, UUIDModel


class Board(AutoSlugMixin, TransientModel):
    group = models.ForeignKey("Group", related_name="boards", on_delete=models.PROTECT)
    name = models.CharField(
        verbose_name=_("Name"),
        max_length=64,
        db_index=True,
        help_text=_(
            "What should this board be called? This will appear in the boards page."
        ),
    )
    slug = models.SlugField(
        verbose_name=_("Identifier"),
        max_length=64,
        blank=True,
        help_text=_(
            "This is a unique board identifier that will appear in the board's URL."
        ),
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("group", "slug"), name="cws2_board_unique_group_slug"
            )
        ]

    def get_absolute_url(self):
        return reverse(
            "board.show", kwargs={"group": self.group.slug, "board": self.slug}
        )


class Thread(UUIDModel, TransientModel):
    board = models.ForeignKey("Board", related_name="threads", on_delete=models.CASCADE)
    title = models.CharField(
        verbose_name=_("Title"),
        max_length=64,
        help_text=_(
            "What should this thread be titled? Try and summarize what the "
            "conversation is about, but keep it short."
        ),
    )
    is_pinned = models.BooleanField(default=False)


class Post(UUIDModel, TransientModel):
    thread = models.ForeignKey("Thread", related_name="posts", on_delete=models.CASCADE)
    message = models.TextField(
        verbose_name=_("Message"),
        help_text=_("What do you want to say? Remember, this is public: be courteous."),
    )
