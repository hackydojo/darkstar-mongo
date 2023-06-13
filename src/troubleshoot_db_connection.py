from app.context import get_context, ServerContext
from dotenv import load_dotenv
from rich import print
from pymongo import database


def main():
    server_context: ServerContext = get_context()
    print(f"TLS Required: {server_context.tls_required}")
    print(f"Using Connection: {server_context.build_connection_string()}")
    print(server_context.database_without_tls)
    mongo_db: database = server_context.database
    test_collection = mongo_db["test-collection"]
    print(str(test_collection.insert_one({"name": "Janice Smith"})))


if __name__ == "__main__":
    load_dotenv()
    main()
