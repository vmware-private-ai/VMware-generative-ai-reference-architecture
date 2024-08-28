# Running a PGVector DB

__PGVector__ is an open-source __vector similarity search extension for PostgreSQL__ that allows you store
vectors with the rest of your data. 

## PGVector provides:
- Exact and approximate nearest neighbor search
- Search based on L2, inner product, and cosine distances
- Multi-language with a Postgres client
- ACID compliance, point-in-time recovery, JOINs, and all features of Postgres

The RAG pipelines implementations in this __Improved RAG Starter Pack
rely on PGVector and PostgreSQL__ as the index and persistence mechanisms to store and retrieve text data to augment 
LLMs' generation processes, so please __make sure you get PGVector up and running before trying any of the 
Python scripts of this Starter Pack.__


## Running PGVector

**Option 1 (preferred)**:
For VMware Cloud Foundation users we recommend using __Aria Automation__ to deploy long-lasting 
PostgreSQL with PGVector instances. Please refer to the 
[Deploy a Vector Database in VMware Private AI Foundation with NVIDIA](https://docs.vmware.com/en/VMware-Cloud-Foundation/5.2/vmware-private-ai-foundation-nvidia/GUID-337AAADE-AB79-4480-AEAB-265035AC3439.html)
documentation to learn how to do it.

**Option 2:**
For quick (and convenient) experiments you can use Docker Compose to launch a PostgreSQL wih PGVector 
container. The `docker-compose.yaml` file included in this directory defines
a demo PostgreSQL configuration, which you can customize according to your preferences. 

Once you are happy with the definitions set by the `docker-compose.yaml` file, please this from a 
shell terminal, move your prompt to this directory and run  

```docker compose up -d```  

The `-d` option instructs Docker to run the container in detached mode, i.e. to run container in the background.
Once the container is running, the service will be available from port `5432` using the following access credentials:

      - POSTGRES_DB: postgres
      - POSTGRES_USER: demouser
      - POSTGRES_PASSWORD: demopasswd
