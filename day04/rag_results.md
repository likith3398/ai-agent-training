# Task 4.2 — RAG Results

## Objective

Test the RAG system for grounded answers, source citations, and refusal when the information is not available in the knowledge base.

## Configuration

- Vector database: Chroma
- Retriever: Chroma retriever
- Number of retrieved documents (`k`): 3
- Embedding model: `gemini-embedding-001`
- LLM: `gemini-3.6-flash`
- Knowledge base: `day04/kb/`
- Answers must be based only on retrieved context.
- Factual statements must include the source filename in square brackets.
- Unknown questions must return the exact refusal message.

## Test Results

### 1. Hotlisting

**Question:**  
What are the steps to hotlist a card?

**Expected:**  
The system should explain the card hotlisting process using information from the knowledge base and cite the source filename.

**Result:**  
PASS

**Retrieved source(s):**
- `debit_card_hotlisting_process.txt`

**Answer summary:**  
The customer can hotlist the card through mobile banking or net banking, or by contacting the NovaTrust Card Support Desk. Identity verification is required before hotlisting. The card is then blocked from further transactions.

---

### 2. UPI Daily Limit

**Question:**  
What is the daily UPI transaction limit?

**Expected:**  
The system should provide the daily UPI transaction limit from the knowledge base.

**Result:**  
PASS

**Retrieved source(s):**
- `upi_limits_and_failures.txt`

**Answer summary:**  
The maximum daily UPI transaction amount is ₹1,00,000. The knowledge base also specifies a maximum of 20 successful UPI transactions per day.

---

### 3. KYC Documents

**Question:**  
What documents are required for KYC?

**Expected:**  
The system should list the KYC documents mentioned in the knowledge base.

**Result:**  
PASS

**Retrieved source(s):**
- `kyc_requirements.txt`

**Answer summary:**  
A valid government-issued identity document is required. A valid address document may be required, and a recent customer photograph may be requested. Additional documents may also be required depending on the account type.

---

### 4. Fixed Deposit Minimum Tenure

**Question:**  
What is the minimum tenure for a fixed deposit?

**Expected:**  
The system should provide the minimum fixed-deposit tenure from the knowledge base.

**Result:**  
PASS

**Retrieved source(s):**
- `fixed_deposit_basics.txt`

**Answer summary:**  
The system successfully retrieved the relevant fixed-deposit information and provided the answer with a source citation.

---

### 5. Loan Eligibility

**Question:**  
What are the eligibility criteria for the loan?

**Expected:**  
The system should provide the loan eligibility criteria from the knowledge base.

**Result:**  
PASS

**Retrieved source(s):**
- `personal_loan_eligibility.txt`

**Answer summary:**  
The system successfully retrieved the relevant personal-loan eligibility information and provided the answer with a source citation.

---

### 6. Grievance Escalation

**Question:**  
What are the grievance escalation levels?

**Expected:**  
The system should explain the escalation levels using the knowledge base.

**Result:**  
PASS

**Retrieved source(s):**
- `grievance_escalation_matrix.txt`

**Answer summary:**  
Level 1 is Customer Support. If unresolved after 3 working days, the issue moves to Level 2, the Customer Resolution Team. If unresolved after 7 working days, it escalates to Level 3, the Grievance Officer.

---

### 7. USD-INR Exchange Rate

**Question:**  
What is today's USD–INR exchange rate?

**Expected:**  
The system should refuse to answer because the current exchange rate is not available in the knowledge base.

**Result:**  
PASS

**Expected refusal:**

> I don't have that information in my knowledge base — let me connect you to a human agent.

---

### 8. Platinum Sapphire Card Charges

**Question:**  
What are the charges for the Platinum Sapphire card?

**Expected:**  
The system should refuse to answer because the required Platinum Sapphire card charge information is not available in the retrieved knowledge-base context.

**Result:**  
PASS

**Expected refusal:**

> I don't have that information in my knowledge base — let me connect you to a human agent.

---

## Overall Result

| Test | Question | Result |
|---|---|---|
| 1 | Hotlisting a card | PASS |
| 2 | UPI daily limit | PASS |
| 3 | KYC documents | PASS |
| 4 | Fixed deposit minimum tenure | PASS |
| 5 | Loan eligibility | PASS |
| 6 | Grievance escalation | PASS |
| 7 | Today's USD-INR exchange rate | PASS |
| 8 | Platinum Sapphire card charges | PASS |

**Total:** 8/8 tests passed.

## Conclusion

The RAG system successfully demonstrated:

- Retrieval of relevant knowledge-base chunks.
- Retrieval using `k=3`.
- Grounded answers based only on retrieved context.
- Source filename citations for factual information.
- Refusal when the requested information is not available in the knowledge base.
- Successful handling of both answerable and deliberately unanswerable questions.