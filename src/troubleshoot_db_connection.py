from app.context import get_context, ServerContext
from dotenv import load_dotenv
from rich import print
from pymongo import database


def main():
    server_context: ServerContext = get_context()
    print(server_context.database_with_tls)
    mongo_db: database = server_context.database
    test_collection = mongo_db["test-collection"]
    print(test_collection.insert_one({"name": "John Smith"}))


if __name__ == "__main__":
    load_dotenv()
    main()
