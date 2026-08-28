# Day 04 Notes

## Chunk Size Experiment

### Experiment 1

* Chunk size: 500
* Chunk overlap: 50
* Number of documents: 10
* Number of chunks: 20

### Experiment 2

* Chunk size: 100
* Chunk overlap: 50
* Number of documents: 10
* Number of chunks: 102

## What I Observed

When the chunk size was reduced from 500 to 100, the number of chunks increased from 20 to 102.

The reason is that a smaller chunk size divides the same amount of document text into smaller pieces. Therefore, more chunks are required to represent the same ten documents.

The chunk overlap was kept at 50 for both experiments. Overlap allows adjacent chunks to share some text so that useful context is less likely to be lost at chunk boundaries.

## Why Chunk Size Is a Design Decision

Chunk size is a design decision because it affects the quality of information retrieval.

If chunks are too large, a retrieved chunk may contain a lot of unrelated information. This can reduce retrieval precision because the system may retrieve more text than is actually relevant to the user's question.

If chunks are too small, important information may be separated across multiple chunks. This can cause the system to retrieve only part of the information needed to answer a question.

The appropriate chunk size depends on the type of documents, the structure of the information, the questions users are expected to ask, and the retrieval quality required by the application.

For this knowledge base, the chunk size should preserve enough context to answer banking questions while keeping chunks focused enough for accurate retrieval.

## Key Learning

Document indexing is not simply about putting documents into a vector database.

The documents first need to be divided into meaningful chunks, converted into embeddings, and stored in the vector database.

The chunking strategy can directly affect how well relevant information is retrieved later in a RAG application.
