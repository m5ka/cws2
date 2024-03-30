from phonecodes import phonecodes


def ipa_from_ipa_or_xsampa(ipa: str, xsampa: str) -> str:
    if ipa:
        return ipa
    if xsampa:
        return xsampa_to_ipa(xsampa)
    return ""


def ipa_to_xsampa(ipa: str) -> str:
    return phonecodes.convert(ipa, "ipa", "xsampa")


def xsampa_to_ipa(xsampa: str) -> str:
    return phonecodes.convert(xsampa, "xsampa", "ipa")
