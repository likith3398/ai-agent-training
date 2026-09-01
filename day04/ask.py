import os

from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_google_genai import (
    GoogleGenerativeAIEmbeddings,
    ChatGoogleGenerativeAI,
)

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env")


# ============================================================
# 1. Load the same embedding model used when building Chroma
# ============================================================

embeddings = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001",
    google_api_key=api_key,
)


# ============================================================
# 2. Load the persisted Chroma database
# ============================================================

db = Chroma(
    persist_directory="chroma_db",
    embedding_function=embeddings,
)


# ============================================================
# 3. Create retriever with k=3
# ============================================================

retriever = db.as_retriever(
    search_kwargs={"k": 3}
)


# ============================================================
# 4. Load Gemini model
# ============================================================

llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    google_api_key=api_key,
)


# ============================================================
# 5. Grounded RAG prompt
# ============================================================

PROMPT = """
You are a knowledge-base assistant for NovaTrust Bank.

Answer the user's question using ONLY the information provided
in the context below.

Rules:
1. Do not use outside knowledge.
2. Do not guess.
3. Do not invent or assume information.
4. Every factual statement must have the source filename in
   square brackets immediately after the fact.
5. Use the exact source filename provided in the context.
6. If the context does not contain enough information to answer
   the question, reply EXACTLY:

I don't have that information in my knowledge base — let me connect you to a human agent.

Context:
{context}

Question:
{question}

Answer:
"""


# ============================================================
# 6. The 8 required questions
# ============================================================

questions = [
    "What are the steps to hotlist a card?",
    "What is the daily UPI transaction limit?",
    "What documents are required for KYC?",
    "What is the minimum tenure for a fixed deposit?",
    "What are the eligibility criteria for the loan?",
    "What are the grievance escalation levels?",
    "What is today's USD–INR exchange rate?",
    "What are the charges for the Platinum Sapphire card?",
]


# ============================================================
# 7. Ask each question
# ============================================================

for question in questions:

    print("\n" + "=" * 70)
    print("QUESTION:")
    print(question)

    try:

        # ----------------------------------------------------
        # Retrieve top 3 chunks
        # ----------------------------------------------------

        docs = retriever.invoke(question)

        print(f"\nNumber of documents retrieved: {len(docs)}")

        # ----------------------------------------------------
        # Print only the source filenames
        # ----------------------------------------------------

        print("\nRETRIEVED SOURCES:")

        for doc in docs:
            source = doc.metadata.get("source", "unknown")
            print(f"- {source}")

        # ----------------------------------------------------
        # If no documents are retrieved, use exact refusal
        # ----------------------------------------------------

        if not docs:
            answer = (
                "I don't have that information in my knowledge base — "
                "let me connect you to a human agent."
            )

            print("\nFINAL ANSWER:")
            print(answer)

            continue

        # ----------------------------------------------------
        # Build context from ALL retrieved chunks
        # ----------------------------------------------------

        context_parts = []

        for doc in docs:

            source = doc.metadata.get("source", "unknown")

            context_parts.append(
                f"Source filename: {source}\n"
                f"Content:\n{doc.page_content}"
            )

        context = "\n\n".join(context_parts)

        # ----------------------------------------------------
        # Build final grounded prompt
        # ----------------------------------------------------

        final_prompt = PROMPT.format(
            context=context,
            question=question,
        )

        # ----------------------------------------------------
        # Ask Gemini ONCE for this question
        # ----------------------------------------------------

        response = llm.invoke(final_prompt)

        # ----------------------------------------------------
        # Extract answer text safely
        # ----------------------------------------------------

        if isinstance(response.content, list):

            answer_parts = []

            for item in response.content:

                if isinstance(item, dict):

                    if "text" in item:
                        answer_parts.append(item["text"])

                elif isinstance(item, str):
                    answer_parts.append(item)

            answer = "".join(answer_parts)

        else:
            answer = str(response.content)

        # ----------------------------------------------------
        # Print final answer
        # ----------------------------------------------------

        print("\nFINAL ANSWER:")
        print(answer)

    except Exception as e:

        print("\nERROR:")
        print(f"{type(e).__name__}: {e}")

        # Do not stop the entire 8-question test.
        # Move to the next question.
        continue