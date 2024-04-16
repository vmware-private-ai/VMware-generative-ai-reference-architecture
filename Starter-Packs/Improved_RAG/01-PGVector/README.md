# Running a Local PGVector DB

__PGVector__ is an open-source __vector similarity search extension for PostgreSQL__ that allows you store
vectors with the rest of your data. 

The RAG pipelines implementations in this __Improved RAG Starter Pack
rely on PGVector__ as the index and persistence mechanism to store and retrieve text data to augment 
LLMs' generation processes, so please __make sure you get PGVector up and running before trying any of the 
Python scripts of this Starter Pack.__

## PGVector supports:
- Exact and approximate nearest neighbor search
- Search based on L2, inner product, and cosine distances
- Multi-language with a Postgres client 
- ACID compliance, point-in-time recovery, JOINs, and all features of Postgres

## Running PGVector
Please move to this directory from a terminal and run the `docker compose up -d` script to launch a PGVector instance using Docker Compose. The 
`docker-compose.yaml` file defines the PostgreSQL configuration, which you can customize according to 
your preferences.

