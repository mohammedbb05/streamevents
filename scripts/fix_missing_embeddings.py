"""Standalone script to set missing 'embedding' fields to null in the MongoDB collection.
Run with: python scripts/fix_missing_embeddings.py
"""
from pymongo import MongoClient


def main():
    mongo_uri = 'mongodb://localhost:27017'
    db_name = 'streamevents_db'
    client = MongoClient(mongo_uri)
    db = client[db_name]
    coll = db['events_event']
    result = coll.update_many({'embedding': {'$exists': False}}, {'$set': {'embedding': None}})
    print(f"Matched {result.matched_count}, modified {result.modified_count} documents.")


if __name__ == '__main__':
    main()
