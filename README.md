# RAG Vector Search Demo

A clean-room, production-inspired Retrieval-Augmented Generation retrieval
pipeline built with FastAPI and Qdrant.

The repository demonstrates the retrieval side of a RAG architecture:

Document
  -> Chunk
  -> Embed
  -> Store in Qdrant
  -> Embed Query
  -> Semantic Search
  -> Source-aware Context

## Features

- FastAPI API
- Qdrant vector database
- Embedding-provider abstraction
- Deterministic local embedding demo
- Separate document/query embedding tasks
- Configurable chunk size and overlap
- Stable vector point IDs
- Metadata preservation
- Semantic retrieval
- Source-aware context construction
- Docker Compose deployment
- Synthetic demo documents
- Automated tests
- No external API key required

## Why a local embedding provider?

The default public demo intentionally uses a deterministic local embedding
provider so the complete pipeline can be cloned, tested, and demonstrated
without sending data to an external service or requiring API credentials.

The provider interface can be replaced with hosted embedding providers.

## Run

    docker compose up --build -d

API documentation:

    http://localhost:8083/docs

## Demo flow

Ingest the included synthetic documents:

    curl -X POST \
      http://localhost:8083/v1/ingest \
      -H 'Content-Type: application/json' \
      --data @examples/documents.json

Search:

    curl -X POST \
      http://localhost:8083/v1/search \
      -H 'Content-Type: application/json' \
      -d '{"query":"How can I track my delivery?","limit":3}'

Build RAG context:

    curl -X POST \
      http://localhost:8083/v1/context \
      -H 'Content-Type: application/json' \
      -d '{"query":"When can an unused item be returned?","limit":3}'

## Endpoints

- GET /health
- GET /v1/providers
- POST /v1/ingest
- POST /v1/search
- POST /v1/context

## Privacy

All included content is synthetic.

This repository contains no customer data, private production infrastructure,
credentials, or production database access.
