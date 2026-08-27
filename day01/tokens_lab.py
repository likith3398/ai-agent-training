import tiktoken

enc = tiktoken.encoding_for_model("gpt-4o-mini")

samples = [
    "I want to block my debit card immediately",
    "मेरा डेबिट कार्ड खो गया है",
    "Mera card kho gaya hai, please block karo",
    "Account number 3021 4456 8890 1123",

    # Add your own examples
    "I need help with my bank account",
    "YOUR MOTHER TONGUE SENTENCE HERE",
]

for s in samples:
    tokens = enc.encode(s)
    print(f"{len(tokens):>3} tokens -> {s}")