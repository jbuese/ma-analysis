# 📊 Advanced Citation Analysis Tools

This repository contains scripts for creating visualizations for my masters thesis 'Design principles for a conversational agent to improve communication and documentation in the construction industry'. The tools use the citation data from a [Zotero](https://www.zotero.org/) collection used during the literature research.

The main features are:

- 🕸 Citation Graph Script for hermeneutic literature research
- 📊 Plot for publication years
- 📋 Fuzzy string matching for most common tags in the literature

## Installation

```bash
# with pip and venv on linux:
python -m venv myenv
source myenv/bin/activate
pip install -r requirements.txt
```

## Tools for citation metrics

The folder `citation-metrics` contains a jupyter-notebook for the plots used in the thesis. For now it contains a plot for the publication years (given that your literature has that attached) and a script for analyzing the tags (using Levenshtein distance).

The jupyter-notebook contains all the documentation needed for using it.

See examples:

- [Publication years plot](citation-metrics/common_tags-2023-12-05.pdf)
- [Common tags plot](citation-metrics/publication_years-2023-12-05.pdf)

## Citation graph

The folder `citation-graph` contains a simple script for creating a citation network as part of a hermeneutic literature research using the graph database [neo4j](https://neo4j.com/). The goal is to facilitate the understanding and visualization of connections between different works in a specific field of study. By leveraging this script, I was able to gain a new perspective on the literature review process, making it more efficient and comprehensive.

### Pre-requirements

- You will need a running neo4j-instance. I suggest using either neo4j-desktop or docker for this
- Neo4j-Bloom is a nice visualization tool which I used for my thesis

### Start the script

1. You will have to input
   - the NEO4J data (if its not default) and
   - the API-Key, User-Key and Collection-Key from Zotero (the jupyter-notebook at `citation-metrics` offers help on where to find those)
2. Start the script using `python build-citation-graph.py`
3. ✅ Done, the script will do the rest
4. -> You can now use Neo4j-Bloom and look at the graph

### Whats next?

After all, this is a simple script tailored to my specific needs. There are a lot of things that could be done better (e.g. connecting nodes based on doi, but that was beyond my scope). However, the concept of citation graphs will certainly become more important in the future and you should have a look at [connectedpapers](https://www.connectedpapers.com/) and [citation graph](https://citationgraph.org/) for more information.
