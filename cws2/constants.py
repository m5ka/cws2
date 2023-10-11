from django.utils.translation import gettext_lazy as _


class GroupAccessType:
    ANYONE = "A"
    INVITE = "I"
    SYSTEM = "S"
    CHOICES = (
        (ANYONE, _("Anyone")),
        (INVITE, _("Invite only")),
        (SYSTEM, _("System only")),
    )
    CHOICES_PICKABLE = (
        (ANYONE, _("Anyone")),
        (INVITE, _("Invite only")),
    )


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


class PartOfSpeech:
    ABBREVIATION = "ABB"
    ADJECTIVE = "ADJ"
    ADPOSITION = "ADP"
    ADVERB = "ADV"
    AFFIX = "AFF"
    AUXILIARY = "AUX"
    CONJUNCTION = "C"
    DETERMINER = "DET"
    INTERJECTION = "I"
    NOUN = "N"
    NUMERAL = "NUM"
    PARTICLE = "PTC"
    PHRASE = "PHR"
    PRONOUN = "P"
    PROPER_NOUN = "PPR"
    VERB = "V"
    CHOICES = (
        (ABBREVIATION, _("Abbreviation")),
        (ADJECTIVE, _("Adjective")),
        (ADPOSITION, _("Adposition")),
        (ADVERB, _("Adverb")),
        (AFFIX, _("Affix")),
        (AUXILIARY, _("Auxiliary")),
        (CONJUNCTION, _("Conjunction")),
        (DETERMINER, _("Determiner")),
        (INTERJECTION, _("Interjection")),
        (NOUN, _("Noun")),
        (NUMERAL, _("Numeral")),
        (PARTICLE, _("Particle")),
        (PHRASE, _("Phrase")),
        (PRONOUN, _("Pronoun")),
        (PROPER_NOUN, _("Proper noun")),
        (VERB, _("Verb")),
    )


class PhonoSystemStatus:
    DRAFT = "D"
    PUBLISHED = "P"
    CHOICES = (
        (DRAFT, _("Draft")),
        (PUBLISHED, _("Published")),
    )


class PhoneCategory:
    CONSONANT = "C"
    VOWEL = "V"
    QUALITY = "Q"
    UNCATEGORIZED = "U"
    CHOICES = (
        (CONSONANT, _("Consonant")),
        (VOWEL, _("Vowel")),
        (QUALITY, _("Quality")),
        (UNCATEGORIZED, _("Uncategorized")),
    )


class WordRegister:
    AFFECTIONATE = "AFFC"
    ARCHAIC = "ARCH"
    CASUAL = "CASL"
    DATED = "DATD"
    EUPHEMISTIC = "EUPH"
    FORMAL = "FORM"
    HONORIFIC = "HONR"
    HUMBLE = "HUMB"
    HUMOROUS = "HMRS"
    INTIMATE = "INTM"
    JARGON = "JRGN"
    POETIC = "POET"
    RELIGIOUS = "RELG"
    SLANG = "SLNG"
    TABOO = "TBOO"
    VULGAR = "VULG"
    OTHER = "OTHR"
    CHOICES = (
        (AFFECTIONATE, _("Affectionate/Endearing")),
        (ARCHAIC, _("Archaic")),
        (CASUAL, _("Casual")),
        (DATED, _("Dated")),
        (EUPHEMISTIC, _("Euphemistic")),
        (FORMAL, _("Formal/Polite")),
        (HONORIFIC, _("Honorific")),
        (HUMBLE, _("Humble")),
        (HUMOROUS, _("Humorous/Sarcastic")),
        (INTIMATE, _("Intimate")),
        (JARGON, _("Jargon")),
        (POETIC, _("Poetic")),
        (RELIGIOUS, _("Religious")),
        (SLANG, _("Slang")),
        (TABOO, _("Taboo")),
        (VULGAR, _("Vulgar")),
        (OTHER, _("Other (see notes)")),
    )
