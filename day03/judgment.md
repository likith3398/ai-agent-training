# Day 3 — Workflow or Agent?

## 1. Classify incoming customer emails into five categories

**Decision: Workflow**

The task has predefined categories and follows a predictable classification process, so the cost of errors is relatively manageable. Because the inputs, categories, and expected output are well-defined, predictability is high and a workflow is appropriate.

## 2. Resolve a customer's failed UPI transaction end-to-end across three internal systems, deciding the path as it goes

**Decision: Agent**

The system needs to inspect multiple internal systems and dynamically decide what to do next based on the information it discovers. The cost of errors is high because incorrect actions could affect a customer's financial transaction, while predictability is lower because the resolution path can vary.

## 3. Generate a monthly account-summary paragraph from a fixed data table

**Decision: Workflow**

The task uses a fixed data table and follows a repeatable process to generate the summary, making it highly predictable. The cost of errors is relatively low if the output is reviewed, so there is little need for autonomous agent decision-making.

## 4. Answer product FAQs from a knowledge base

**Decision: Workflow**

The system can retrieve relevant information from a predefined knowledge base and generate an answer using a controlled process. The cost of errors can be moderate because incorrect product information could mislead customers, so the high predictability of a knowledge-base workflow is preferable to autonomous decision-making.

## 5. Research and compile a comparison of competitor credit-card offerings

**Decision: Agent**

The research path can change depending on what information is found, requiring the system to decide which sources to investigate and what to do when information is missing. The cost of errors is moderate because inaccurate competitor information could affect business decisions, while predictability is lower than in a fixed workflow.

## 6. Route an incoming call to the right department

**Decision: Workflow**

The call can be classified based on predefined intent and routed according to established department rules. The cost of errors is generally manageable because an incorrectly routed call can usually be transferred, and predictability is high when the routing rules are predefined.
