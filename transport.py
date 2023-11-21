import os
import sys
import json
import logging
from neo4j import GraphDatabase
from neo4j.exceptions import DriverError, Neo4jError

logging.basicConfig(level=logging.INFO)
ADDRESS = os.getenv("NEO4J_ADDRESS", "bolt://localhost:7687")
AUTH = (os.getenv("NEO4J_USER", "neo4j"), os.getenv("NEO4J_PASSWORD", "adminadmin"))

# Ask for CONNECTED_TO_ID via CLI
CONNECTED_TO_ID = input("Enter the CONNECTED_TO_ID (press Enter to skip): ")
try:
  CONNECTED_TO_ID = int(CONNECTED_TO_ID) if CONNECTED_TO_ID.strip() else None
except ValueError:
  logging.error("🛑 Invalid value entered for CONNECTED_TO_ID. Please enter an integer.")
  sys.exit()

# Ask for ROUND via CLI
ROUND = input("Enter the ROUND: ")
try:
  ROUND = int(ROUND)
except ValueError:
  logging.error("🛑 Invalid value entered for ROUND. Please enter an integer.")
  sys.exit()

driver = GraphDatabase.driver(ADDRESS, auth=AUTH)
logging.info(f"💾 Successfully connected to Neo4j: {driver}")

def check_connected_id(session, connected_id):
  """
  Check if a node with the given connected_id exists in the Neo4j database.

  Args:
    session: The Neo4j session object.
    connected_id: The ID of the node to check.

  Returns:
    bool: True if the node exists, False otherwise.
  """
  try:
    result = session.run(
      "MATCH (n) WHERE id(n) = $connected_id RETURN n",
      connected_id=connected_id
    )
    return result.single() is not None
  except (DriverError, Neo4jError) as exception:
    logging.error(f"🛑 Neo4jError checking connected ID: {connected_id}", exception)
    return False


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
    result = session.run(
      "MATCH (n:paper {title: $title}) RETURN n",
      title=obj["title"]
    )
    if result.single() is not None:
      logging.info(f"⏩ Skipping title: {obj['title']}")
      return

    result = session.run(
      "CREATE (n:paper {title: $title, source: $source, year: $year, author_tag: $author_tag, authors: $authors, doi: $doi, round: $round}) "
      "RETURN n",
      label=obj['type'].replace('-', '_'),
      title=obj["title"],
      source=obj.get("source"),
      year=obj["issued"]["date-parts"][0][0],
      author_tag=author_tag,
      authors=authors,
      doi=obj.get("DOI") or obj.get("note", "").replace("DOI: ", "") if ("DOI" in obj or "note" in obj) else None,
      round=ROUND,
    )
    node = result.single()[0]
  except (DriverError, Neo4jError) as exception:
    logging.error(f"🛑 Neo4jError processing title: {obj['title']}", exception)
    return

  if CONNECTED_TO_ID is not None:
    create_relationship(session, node.id, CONNECTED_TO_ID)

def create_relationship(session, node_id, connected_to_id):
  """
  Create a "CITES"-relationship between two nodes in the Neo4j database.

  Args:
    session: The Neo4j session object.
    node_id: The ID of the first node. (relation from)
    connected_to_id: The ID of the second node. (relation to)

  Returns:
    None
  """
  try:
    session.run(
      "MATCH (n) WHERE id(n) = $node_id "
      "MATCH (predefinedNode) WHERE id(predefinedNode) = $connected_to_id "
      "CREATE (n)<-[:CITES]-(predefinedNode)",
      node_id=node_id,
      connected_to_id=connected_to_id
    )
  except (DriverError, Neo4jError) as exception:
    logging.error(f"🛑 Neo4jError creating relationship for node_id: {node_id} and connected_to_id: {connected_to_id}", exception)

# Step 2: Read the contents of the exported_bib.json file
with open("exported_bib.json", encoding="cp437") as file:
  json_data = json.load(file)

  with driver.session() as session:
    # Step 3: Check if the connected_id node exists
    if CONNECTED_TO_ID is not None and not check_connected_id(session, CONNECTED_TO_ID):
      logging.error(f"🛑 There is no node for connected_to_id: {CONNECTED_TO_ID}")
    else:
      # Step 4: Iterate over each object in the JSON data
      for obj in json_data:
        authors = [author["family"] for author in obj["author"]]
        author_tag = authors[0] if len(authors) == 1 else " und ".join(authors) if len(authors) == 2 else authors[0] + " et al."

        # Step 5: Create a new node in Neo4j for each object
        create_paper_node(session, obj)

# Step 6: Close the connection to the Neo4j database and the file stream
driver.close()
file.close()