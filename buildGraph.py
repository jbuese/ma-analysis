import os
import json
import logging
import requests
from neo4j import GraphDatabase
from neo4j.exceptions import DriverError, Neo4jError
import json

logging.basicConfig(level=logging.INFO)

# Replace when not using default values
NEO4J_ADDRESS = os.getenv("NEO4J_ADDRESS", "bolt://localhost:7687")
NEO4J_AUTH = (os.getenv("NEO4J_USER", "neo4j"), os.getenv("NEO4J_PASSWORD", "adminadmin"))

# Replace with actual values
ZOTERO_API_KEY = os.getenv("ZOTERO_API_KEY", "<fill-me-in>")
ZOTERO_USER_ID = os.getenv("ZOTERO_USER_ID", "<fill-me-in>")
ZOTERO_COLLECTION_ID = os.getenv("ZOTERO_COLLECTION_ID", "<fill-me-in>")

def create_paper_node(session, obj):
  """
  Create a new paper node in the Neo4j database.

  Args:
    session: The Neo4j session object.
    obj: The JSON object representing the paper.

  Returns:
    None
  """
  try:
    if obj.get("itemType") in ["attachment", "note"]:
      logging.info(f"⏩ Skipping title because it is a note or an attachment")
      return
    
    result = session.run(
      "MATCH (n:paper {title: $title}) RETURN n",
      title=obj.get("title")
    )
    if result.single() is not None:
      logging.info(f"⏩ Skipping title because it is already there: {obj['title']}")
      return
    
    authors = [author["lastName"] for author in obj["creators"] if author["creatorType"] == "author"]
    author_tag = authors[0] if len(authors) == 1 else " und ".join(authors) if len(authors) == 2 else authors[0] + " et al."
    tags = [tag['tag'] for tag in obj['tags'] if not tag['tag'].startswith('round')]
    round = [tag['tag'][6:] for tag in obj['tags'] if tag['tag'].startswith('round')]

    result = session.run(
      "CREATE (n:paper {key: $key, title: $title, itemType: $itemType, libraryCatalog: $libraryCatalog, year: $year, author_tag: $author_tag, authors: $authors, doi: $doi, round: $round, tags: $tags, abstract: $abstract}) "
      "RETURN n",
      key=obj.get("key"),
      title=obj.get("title"),
      itemType=obj.get("itemType", "").replace('-', '_'),
      libraryCatalog=obj.get("libraryCatalog"),
      year=obj.get("date"),
      author_tag=author_tag,
      authors=authors,
      doi=obj.get("DOI") or obj.get("note", "").replace("DOI: ", "") if ("DOI" in obj or "note" in obj) else None,
      round=round,
      tags=tags,
      abstract=obj.get("abstractNote"),
    )
    node = result.single()[0]
  except (DriverError, Neo4jError) as exception:
    logging.error(f"🛑 Neo4jError processing title: {obj['title']}", exception)
    return

def create_relationship(session, citation):
  """
  Create a "RELATED"-relationship between two nodes in the Neo4j database.

  Args:
    session: The Neo4j session object.
    citation: The JSON object representing the citation.

  Returns:
    None
  """
  if citation.get("itemType") in ["attachment", "note"]:
      logging.info(f"⏩ Skipping title because it is a note or an attachment")
      return
    
  relations = citation.get("relations", {}).get("dc:relation", [])
  if isinstance(relations, str):
    relations = [relations]
  key_citation = citation.get("key")
  
  for relation in relations:
    key_relation = relation.split("/")[-1]
  
    try:
      session.run(
        "MATCH (n) WHERE n.key = $key_n "
        "MATCH (m) WHERE m.key = $key_m "
        "CREATE (n)-[:RELATED]->(m)",
        key_n=key_citation,
        key_m=key_relation
      )
    except (DriverError, Neo4jError) as exception:
      logging.error(f"🛑 Neo4jError creating relationship for node with key: {key_citation} and node with key: {key_relation}", exception)

def main():
  driver = GraphDatabase.driver(NEO4J_ADDRESS, auth=NEO4J_AUTH)
  logging.info(f"💾 Successfully connected to Neo4j: {driver}")

  # Create a session from the driver
  session = driver.session()

  # Make a GET request to the Zotero API to retrieve all citations from the collection
  url = f"https://api.zotero.org/users/{ZOTERO_USER_ID}/collections/{ZOTERO_COLLECTION_ID}/items?limit=100&format=json&key={ZOTERO_API_KEY}"
  response = requests.get(url)

  if response.status_code == 200:
    citations = response.json()
    
    # Extract data from each citation
    citation_data = []
    for citation in citations:
      citation_data.append(citation['data'])
    
    # Create a node for each citation
    for citation in citation_data:
      create_paper_node(session, citation)
      
    # Create the relationship for each citation based on related items
    for citation in citation_data:
      create_relationship(session, citation)
  else:
    print('Failed to retrieve citations from the Zotero API')
    
  # Close the session and driver
  session.close()
  driver.close()

main()