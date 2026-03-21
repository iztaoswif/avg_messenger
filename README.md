Asynchronous REST API messenger made using FastAPI


Stack:
-Python 3.12
-FastAPI
-SQLAlchemy Core (async)
-PostgreSQL
-Alembic (for DB migrations)
-JWT (python-jose)
-Docker / Docker compose


Features:
-JWT authentication (register / login)
-Message sending
-Receiving messages with cursor-based pagination
-Asynchronous interactions with DB
-Isolation of tests using transactions
-Containerizing the app using Docker


Architecture:
app/
    -auth (endpoints, schemas, dependencies, services related to auth)
    -chat (endpoints, schemas, dependencies, services related to interaction with chat(s))
    -core (security logic, config)
    -repositories (abstraction of interacting with database)
    -db (database schemas, engine, async session generator)
basic flow: router -> schemas (validation) -> service -> repository -> database


JWT access tokens store user_id in the "sub" field,
their validity and expiration date is being checked.

For now the SQLAlchemy Core is used for high-level interaction with DB,
switching to SQLAlchemy ORM is considered in the future.

For tests the pytest, pytest-asyncio and httpx AsyncClient +  ASGITransport are used.
Tests are isolated using database transactions.


#TODO
-Websockets support
-Redis caching
-Pagination limits
-First deployment (using GitHub Render)

<img width="1625" height="672" alt="image" src="https://github.com/user-attachments/assets/bb809de3-2be3-49f8-9d12-4870fa5235ed" />
