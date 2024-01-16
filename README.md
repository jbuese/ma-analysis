# 📊 MA Analysis & Visualization Tools

This repository contains scripts for creating visualizations for my masters thesis 'Design principles for a conversational agent to improve communication and documentation in the construction industry'.
Some of the tools use the citation data from a Zotero [^1] collection used during the literature research.
The survey-metrics tools use the survey data collected during a survey on meta-requirements with the OSS Limesurvey [^2].

The main features are:

- 🕸 Citation Graph Script for hermeneutic literature research
- 📊 Plot for publication years
- 📋 Fuzzy string matching for most common tags in the literature
- 🧮 Acceptance score analysis based on Likert style survey

## Installation

```bash
# with pip and venv on linux:
python -m venv myenv
source myenv/bin/activate
pip install -r requirements.txt
```

## Citation metrics

The folder `citation-metrics` contains a jupyter-notebook for the plots used in the literature research section of the thesis. For now it contains a plot for the publication years (given that your literature has that attached) and a script for analyzing the tags (using Levenshtein distance).

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

## Survey metrics

While writing the thesis, I did a small survey on the acceptance rates of experts for some meta-requirements for conversational agents (which I had formulated) using Likert scales [^3]. The `survey-metrics` folder contains a jupyter notebook for the plots used in the parts of the thesis where the survey results are analysed. At the moment it contains a plot for the individual weighted acceptance rates for each meta-requirement and a box plot for an overview of all results.

[^1]: https://www.zotero.org/
[^2]: https://community.limesurvey.org/
[^3]: Likert, R. (1932). A technique for the measurement of attitudes. Archives of Psychology, 22 140, 55.
