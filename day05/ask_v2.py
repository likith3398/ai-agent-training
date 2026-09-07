import os
import json
import time
from pathlib import Path
from typing import List

from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_google_genai import (
    GoogleGenerativeAIEmbeddings,
    ChatGoogleGenerativeAI,
)


# ============================================================
# 1. LOAD ENVIRONMENT VARIABLES
# ============================================================

# Find the project root:
# ai-agent-training/
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Load .env from project root
ENV_FILE = PROJECT_ROOT / ".env"
load_dotenv(ENV_FILE)

# Your Day 4 code uses GEMINI_API_KEY
api_key = os.getenv("GEMINI_API_KEY")

# Also support GOOGLE_API_KEY if available
if not api_key:
    api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise RuntimeError(
        f"API key not found. Please make sure GEMINI_API_KEY "
        f"or GOOGLE_API_KEY exists in {ENV_FILE}"
    )


# ============================================================
# 2. CONFIGURATION
# ============================================================

EMBEDDING_MODEL = "models/gemini-embedding-001"
LLM_MODEL = "gemini-3.6-flash"

# IMPORTANT:
# Day 4's Chroma database is here:
# ai-agent-training/day04/chroma_db
CHROMA_PATH = PROJECT_ROOT / "day04" / "chroma_db"


# ============================================================
# 3. LOAD THE SAME EMBEDDING MODEL USED BY DAY 4
# ============================================================

embeddings = GoogleGenerativeAIEmbeddings(
    model=EMBEDDING_MODEL,
    google_api_key=api_key,
)


# ============================================================
# 4. LOAD THE SAME CHROMA DATABASE USED BY DAY 4
# ============================================================

# IMPORTANT:
# We intentionally DO NOT specify collection_name.
#
# Your Day 4 code uses:
#
# db = Chroma(
#     persist_directory="chroma_db",
#     embedding_function=embeddings,
# )
#
# Therefore Day 5 must use the same default collection.

db = Chroma(
    persist_directory=str(CHROMA_PATH),
    embedding_function=embeddings,
)


# ============================================================
# 5. LOAD GEMINI
# ============================================================

llm = ChatGoogleGenerativeAI(
    model=LLM_MODEL,
    google_api_key=api_key,
)


# ============================================================
# 6. GENERATE THREE SEARCH QUERIES
# ============================================================

def generate_queries(question: str) -> List[str]:

    prompt = f"""
You are helping a banking RAG system retrieve information
from the NovaTrust Bank knowledge base.

Generate exactly 3 different search queries for the user's
question.

The three queries should:
- Have the same meaning as the original question.
- Use different wording.
- Include useful banking keywords.
- Be suitable for semantic/vector search.

Return ONLY valid JSON.

User question:
{question}

Return exactly this structure:

{{
    "queries": [
        "query 1",
        "query 2",
        "query 3"
    ]
}}
"""

    response = llm.invoke(prompt)

    text = response.content

    # Gemini can sometimes return structured content
    if isinstance(text, list):

        parts = []

        for item in text:

            if isinstance(item, dict) and "text" in item:
                parts.append(item["text"])

            elif isinstance(item, str):
                parts.append(item)

        text = "".join(parts)

    text = str(text).strip()

    # Remove markdown code fences if Gemini adds them
    if text.startswith("```json"):
        text = text[len("```json"):].strip()

    if text.startswith("```"):
        text = text[len("```"):].strip()

    if text.endswith("```"):
        text = text[:-3].strip()

    data = json.loads(text)

    queries = data.get("queries", [])

    if not isinstance(queries, list) or len(queries) != 3:
        raise ValueError(
            f"Expected exactly 3 queries but received: {queries}"
        )

    return [str(query).strip() for query in queries]


# ============================================================
# 7. RETRIEVE DOCUMENTS USING ALL THREE QUERIES
# ============================================================

def retrieve_documents(queries: List[str]):

    all_documents = []

    for query in queries:

        docs = db.similarity_search(
            query,
            k=3,
        )

        all_documents.extend(docs)

    # --------------------------------------------------------
    # Remove duplicate documents
    # --------------------------------------------------------

    unique_documents = []

    seen = set()

    for doc in all_documents:

        source = doc.metadata.get("source", "unknown")
        content = doc.page_content.strip()

        # Use source + content to identify duplicates
        document_key = (source, content)

        if document_key not in seen:

            seen.add(document_key)
            unique_documents.append(doc)

    return unique_documents


# ============================================================
# 8. GROUNDED RAG PROMPT
# ============================================================

PROMPT = """
You are a knowledge-base assistant for NovaTrust Bank.

Answer the user's question using ONLY the information
provided in the context below.

Rules:

1. Do not use outside knowledge.
2. Do not guess.
3. Do not invent or assume information.
4. Every factual statement must have the source filename in
   square brackets immediately after the fact.
5. Use the exact source filename provided in the context.
6. If the context does not contain enough information to
   answer the question, reply EXACTLY:

I don't have that information in my knowledge base — let me connect you to a human agent.

Context:
{context}

Question:
{question}

Answer:
"""


# ============================================================
# 9. ANSWER ONE QUESTION
# ============================================================

def answer_question(question: str):

    print("\n" + "=" * 70)
    print("QUESTION:")
    print(question)
    print("-" * 70)

    # --------------------------------------------------------
    # Generate multiple queries
    # --------------------------------------------------------

    queries = generate_queries(question)

    print("GENERATED SEARCH QUERIES:")

    for index, query in enumerate(queries, start=1):
        print(f"{index}. {query}")

    # --------------------------------------------------------
    # Retrieve documents using all three queries
    # --------------------------------------------------------

    docs = retrieve_documents(queries)

    print(f"\nUNIQUE DOCUMENTS RETRIEVED: {len(docs)}")

    # --------------------------------------------------------
    # Print retrieved source filenames
    # --------------------------------------------------------

    print("\nRETRIEVED SOURCES:")

    if not docs:

        print("- None")

    else:

        for doc in docs:

            source = doc.metadata.get(
                "source",
                "unknown"
            )

            print(f"- {source}")

    # --------------------------------------------------------
    # No documents -> exact fallback
    # --------------------------------------------------------

    if not docs:

        answer = (
            "I don't have that information in my knowledge base "
            "— let me connect you to a human agent."
        )

        print("\nFINAL ANSWER:")
        print(answer)

        return

    # --------------------------------------------------------
    # Build context
    # --------------------------------------------------------

    context_parts = []

    for doc in docs:

        source = doc.metadata.get(
            "source",
            "unknown"
        )

        context_parts.append(
            f"Source filename: {source}\n"
            f"Content:\n{doc.page_content}"
        )

    context = "\n\n".join(context_parts)

    # --------------------------------------------------------
    # Build final prompt
    # --------------------------------------------------------

    final_prompt = PROMPT.format(
        context=context,
        question=question,
    )

    # --------------------------------------------------------
    # Ask Gemini for final answer
    # --------------------------------------------------------

    response = llm.invoke(final_prompt)

    # --------------------------------------------------------
    # Safely extract response text
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # Print final answer
    # --------------------------------------------------------

    print("\nFINAL ANSWER:")
    print(answer)


# ============================================================
# 10. THE 8 REQUIRED QUESTIONS
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
# 11. RUN ALL 8 QUESTIONS
# ============================================================

for question in questions:

    try:

        answer_question(question)

    except Exception as e:

        print("\nERROR:")
        print(f"{type(e).__name__}: {e}")

    # Small delay to reduce Gemini rate-limit problems
    time.sleep(2)