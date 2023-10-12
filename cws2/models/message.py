from django.db import models
from django.utils.translation import gettext_lazy as _

from cws2.models.base import TransientModel


class Message(TransientModel):
    sender = models.ForeignKey(
        "User",
        on_delete=models.PROTECT,
        related_name="sent_messages",
        verbose_name=_("Sender"),
        help_text=_("The user that sent this message."),
    )
    recipient = models.ForeignKey(
        "User",
        on_delete=models.PROTECT,
        related_name="messages",
        verbose_name=_("Recipient"),
        help_text=_("The user to whom this message should be sent."),
    )
    body = models.TextField(
        verbose_name=_("Message body"),
        help_text=_(
            "The main body of the message. This should contain what you wish to be "
            "sent to the recipient."
        ),
    )
    read_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name=_("Read at"),
        help_text=_("When this message was first read by the recipient."),
    )

    def __str__(self):
        return (
            f"{self.sender.username} to {self.recipient.username} ({self.created_at})"
        )
