from google import genai

# Create Gemini client
client = genai.Client()

# -----------------------------
# BAD PROMPT
# -----------------------------

bad_prompt = """
I visited your MG Road branch on Tuesday to update my mobile number,
waited 45 minutes, and nobody helped me.

Tell me what you think about this complaint.
"""

# -----------------------------
# GOOD PROMPT
# -----------------------------

good_prompt = """
You are a customer service complaint classifier.

Your task is to classify the customer complaint into exactly ONE
of the following categories:

1. Branch Service
2. Account Issue
3. Technical Issue
4. Billing Issue
5. Other

Return ONLY the category name.
Do not provide an explanation.

Customer complaint:

I visited your MG Road branch on Tuesday to update my mobile number,
waited 45 minutes, and nobody helped me.
"""

# -----------------------------
# CALL GEMINI WITH BAD PROMPT
# -----------------------------

response_a = client.models.generate_content(
    model="gemini-3.6-flash",
    contents=bad_prompt
)

# -----------------------------
# CALL GEMINI WITH GOOD PROMPT
# -----------------------------

response_b = client.models.generate_content(
    model="gemini-3.6-flash",
    contents=good_prompt
)

# -----------------------------
# DISPLAY RESULTS
# -----------------------------

print("\n========== BAD PROMPT ==========")
print(response_a.text)

print("\n========== GOOD PROMPT ==========")
print(response_b.text)