# Citation Graph Script

This repository contains a simple script for creating a citation network as part of a hermeneutic literature research using the graph database [neo4j](https://neo4j.com/). The script was developed as part of my master's thesis. The goal is to facilitate the understanding and visualization of connections between different works in a specific field of study. By leveraging this script, I was able to gain a new perspective on the literature review process, making it more efficient and comprehensive. 

<br>

### Pre-requirements

- You will need a running neo4j-instance. I suggest using either neo4j-desktop or docker for this
- Neo4j-Bloom is a nice visualization tool which I used for my thesis

### Install the dependencies

```bash
# with pip and venv on linux:
python -m venv myenv
source myenv/bin/activate
pip install -r requirements.txt
```

### Export citations from Zotero

1. Select all the publications that you want to cite from Zotero
2. Right-click, "Export item..." and export as CSL JSON
3. Copy the contents to `exported_bib.json` in this folder

### Start the script

1. Start the script using `python transport.py`
2. You will be asked two things over CLI:
    - Where the publications in the file came from and should be related to (this requires that the connected paper is already part of the graph and you know the id)
    - In which round the citations where tracked (according to the hermeneutic cycles defined by Boell and Cecez-Kecmanovic (2014))
3. ✅ Done, the script will do the rest

### Whats next?

After all, this is a simple script tailored to my specific needs. There are a lot of things that could be done better (e.g. connecting nodes based on doi, but that was beyond my scope). However, the concept of citation graphs will certainly become more important in the future and you should have a look at [connectedpapers](https://www.connectedpapers.com/) and [citation graph](https://citationgraph.org/) for more information.
