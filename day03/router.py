from classifier import classify


# ---------------------------------------------------------
# 1. Small hardcoded FAQ database
# ---------------------------------------------------------

FAQS = {
    "upi_failed": "If your UPI transaction failed, please check your internet connection and verify that your UPI PIN is correct.",
    "upi_pending": "A pending UPI transaction may take some time to complete. Please check the transaction status before trying again.",
    "upi_limit": "UPI transactions are subject to daily transaction limits depending on your bank and account.",
    "upi_not_received": "If the recipient has not received the UPI payment, first check whether the transaction shows as successful in your transaction history."
}


# ---------------------------------------------------------
# 2. FAQ Handler
# ---------------------------------------------------------

def answer_faq(utterance):
    """
    Look for a simple FAQ answer based on keywords.
    Returns an answer if found, otherwise None.
    """

    text = utterance.lower()

    if "pending" in text:
        return FAQS["upi_pending"]

    if "limit" in text:
        return FAQS["upi_limit"]

    if "not received" in text or "didn't receive" in text:
        return FAQS["upi_not_received"]

    if "failed" in text or "failure" in text:
        return FAQS["upi_failed"]

    return None


# ---------------------------------------------------------
# 3. Mock API Handler
# ---------------------------------------------------------

def call_mock_api(intent, entities):
    """
    Simulates an API call.
    No real network request is made.
    """

    if intent == "balance_enquiry":
        return {
            "status": "ok",
            "action": "balance_checked",
            "balance": "₹25,430",
            "ref": "BAL-1001"
        }

    if intent == "card_hotlist":
        return {
            "status": "ok",
            "action": "card_hotlisted",
            "ref": "HTL-1029"
        }

    if intent == "statement_request":
        return {
            "status": "ok",
            "action": "statement_requested",
            "ref": "STM-2045"
        }

    return {
        "status": "error",
        "action": "unsupported_intent"
    }


# ---------------------------------------------------------
# 4. Escalation Handler
# ---------------------------------------------------------

def escalate(utterance, result):
    """
    Creates a structured handover for a human agent.
    """

    return {
        "reason": "Unable to resolve automatically",
        "intent": result.get("intent"),
        "entities": result.get("entities", {}),
        "summary_for_agent": f"Customer said: {utterance}"
    }


# ---------------------------------------------------------
# 5. Main Router
# ---------------------------------------------------------

def route(utterance):
    """
    Classify the user's message and route it
    to the appropriate handler.
    """

    # Step 1: Classify the user's utterance
    result = classify(utterance)

    # Step 2: Escalate if confidence is too low
    if result.get("confidence", 0) < 0.6:
        return escalate(utterance, result)

    # Step 3: Escalate if the intent is out of scope
    if result.get("intent") == "out_of_scope":
        return escalate(utterance, result)

    # Get the detected intent
    intent = result.get("intent")

    # Step 4: Handle small talk directly
    if intent == "small_talk":
        return {
            "status": "ok",
            "reply": "Hello! How can I help you today?"
        }

    # Step 5: Handle API-based intents
    if intent in {
        "balance_enquiry",
        "card_hotlist",
        "statement_request"
    }:
        return call_mock_api(
            intent,
            result.get("entities", {})
        )

    # Step 6: Handle UPI issues
    # FAQ first, then escalate if no FAQ answer exists
    if intent == "upi_issue":

        faq_answer = answer_faq(utterance)

        if faq_answer:
            return {
                "status": "ok",
                "source": "faq",
                "reply": faq_answer
            }

        return escalate(utterance, result)

    # Step 7: Anything else gets escalated
    return escalate(utterance, result)


# ---------------------------------------------------------
# 6. REPL - Chat with the router from the terminal
# ---------------------------------------------------------

if __name__ == "__main__":

    while True:

        user = input("You: ")

        if user.lower() in {"quit", "exit"}:
            break

        print("Bot:", route(user))