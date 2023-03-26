from django.utils.translation import gettext_lazy as _


class LanguageStatus:
    NEW = "1"
    PROGRESSING = "2"
    FUNCTIONAL = "3"
    COMPLETE = "4"
    ABANDONED = "X"
    ON_HOLD = "H"
    CHOICES = (
        (NEW, _("New")),
        (PROGRESSING, _("Progressing")),
        (FUNCTIONAL, _("Functional")),
        (COMPLETE, _("Complete")),
        (ABANDONED, _("Abandoned")),
        (ON_HOLD, _("On hold")),
    )


class LanguageType:
    NOT_SPECIFIED = "NSP"
    A_PRIORI = "APR"
    A_POSTERIORI = "APS"
    ARTLANG = "ART"
    ENGLANG = "ENG"
    IAL = "IAL"
    LOGLANG = "LOG"
    SIGNED = "SGN"
    PROTO = "PRO"
    PIDGIN = "PID"
    CREOLE = "CRE"
    JOKE = "JOK"
    MIXED = "MIX"
    OTHER = "OTH"
    CHOICES = (
        (NOT_SPECIFIED, _("Not specified")),
        (A_PRIORI, _("A priori")),
        (A_POSTERIORI, _("A posteriori")),
        (ARTLANG, _("Artistic language (artlang)")),
        (ENGLANG, _("Engineered language (englang)")),
        (IAL, _("International auxiliary language (IAL)")),
        (LOGLANG, _("Logical language (loglang)")),
        (SIGNED, _("Signed language")),
        (PROTO, _("Common ancestor language (proto-language)")),
        (PIDGIN, _("Pidgin")),
        (CREOLE, _("Creole")),
        (JOKE, _("Joke language")),
        (MIXED, _("Mixed")),
        (OTHER, _("Other")),
    )
