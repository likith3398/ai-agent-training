import re


# ============================================================
# ALLOWED INTENTS
# ============================================================

ALLOWED = [
    "balance_enquiry",
    "card_hotlist",
    "statement_request",
    "upi_issue",
    "small_talk",
    "out_of_scope",
]


# ============================================================
# LOCAL KEYWORDS
# ============================================================

BALANCE_KEYWORDS = [
    "balance",
    "how much money",
    "how much do i have",
    "kitna balance",
    "account balance",
]

CARD_HOTLIST_KEYWORDS = [
    "lost card",
    "stolen card",
    "block my card",
    "block card",
    "hotlist my card",
    "hotlist my credit card",
    "hotlist my debit card",
    "card stolen",
    "card lost",
]

STATEMENT_KEYWORDS = [
    "statement",
    "transaction history",
    "transactions",
    "last 3 months",
    "last three months",
]

UPI_KEYWORDS = [
    "upi",
    "gpay",
    "google pay",
    "phonepe",
    "paytm",
    "upi payment",
]

SMALL_TALK_KEYWORDS = [
    "hello",
    "hi",
    "hey",
    "good morning",
    "good afternoon",
    "good evening",
    "thanks",
    "thank you",
    "bye",
]


# ============================================================
# ENTITY EXTRACTION
# ============================================================

def extract_entities(utterance: str) -> dict:
    entities = {}

    # Find card last four digits
    card_match = re.search(
        r"(?:ending|last\s*4|xxxx)[^\d]*(\d{4})",
        utterance.lower()
    )

    if card_match:
        entities["card_last4"] = card_match.group(1)

    # Find months
    months = [
        "january", "february", "march",
        "april", "may", "june",
        "july", "august", "september",
        "october", "november", "december"
    ]

    lower_text = utterance.lower()

    for month in months:
        if month in lower_text:
            entities["period"] = month
            break

    # Find "last 3 months" style period
    if "last 3 months" in lower_text:
        entities["period"] = "last 3 months"

    return entities


# ============================================================
# CLASSIFY FUNCTION
# ============================================================

def classify(utterance: str) -> dict:
    """
    Local deterministic intent classifier.

    This version does not call Gemini.
    """

    text = utterance.lower().strip()

    entities = extract_entities(utterance)

    # --------------------------------------------------------
    # SMALL TALK
    # --------------------------------------------------------

    if any(
        keyword in text
        for keyword in SMALL_TALK_KEYWORDS
    ):
        return {
            "intent": "small_talk",
            "entities": entities,
            "confidence": 0.95,
        }

    # --------------------------------------------------------
    # BALANCE ENQUIRY
    # --------------------------------------------------------

    if any(
        keyword in text
        for keyword in BALANCE_KEYWORDS
    ):
        return {
            "intent": "balance_enquiry",
            "entities": entities,
            "confidence": 0.95,
        }

    # --------------------------------------------------------
    # CARD HOTLIST
    # --------------------------------------------------------

    if any(
        keyword in text
        for keyword in CARD_HOTLIST_KEYWORDS
    ):
        return {
            "intent": "card_hotlist",
            "entities": entities,
            "confidence": 0.95,
        }

    # --------------------------------------------------------
    # STATEMENT REQUEST
    # --------------------------------------------------------

    if any(
        keyword in text
        for keyword in STATEMENT_KEYWORDS
    ):
        return {
            "intent": "statement_request",
            "entities": entities,
            "confidence": 0.95,
        }

    # --------------------------------------------------------
    # UPI ISSUE
    # --------------------------------------------------------

    if any(
        keyword in text
        for keyword in UPI_KEYWORDS
    ):
        return {
            "intent": "upi_issue",
            "entities": entities,
            "confidence": 0.90,
        }

    # --------------------------------------------------------
    # OUT OF SCOPE
    # --------------------------------------------------------

    return {
        "intent": "out_of_scope",
        "entities": entities,
        "confidence": 0.95,
    }


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    test_messages = [
        "hello",
        "What is my account balance?",
        "I want to block my card",
        "I need my account statement",
        "Why did my UPI payment fail?",
        "Can you help me book a flight?",
    ]

    for message in test_messages:
        print()
        print("User:", message)
        print("Result:", classify(message))