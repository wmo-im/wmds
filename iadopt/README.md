Contact: WMO TT-WIGOSMD, joerg.klausen@meteoswiss.ch (chair); amilan@wmo.int (WMO Secretariat)

Acknowledgments:
Morgan Silverman, Gao Chen (Nasa)
Kathi Schleidt (DataCove)
Barbara Magagna (FAIR Foundation)
Markus Fiebig (NILU)

# Application of the I-ADOPT ontology framework to WMDR
Work in progress to convert the so-called 'ObservedVariableX' WMDR codelists (X = atmsophere, etc) into I-ADOPT compliant, self-contained, unambiguous names of observed quantities ('Variable' in I-ADOPT).

[more text to go here]

# Use
1. Clone this repo, e.g. from within VS Code.
2. Create virtual environment
    $ python3 -m venv .venv
    $ . .venv/bin/activate
    (.venv) $ pip install poetry
    (.venv) $ poetry env activate
    (.venv) $ poetry add ipykernel # for use in Jupyter notebooks
3. Open atmosphere.ipynb and run the cells.

# Work ahead [TODO]
NB: The 'autogen' folder contains 'wmdr2_property.csv' and 'wmdr2_object_of_interest.csv' files. These are auto-generated and should not be touched.
1. When an improved 'mappings/WMDR_Observed...' file becomes available, this can be used to improve above 2 files.
2. The idea is to create these 2 files (and 'wmdr2_matrix.csv' etc) under 'wmdr2-candiates', and use the vocabulary builder application (vocabulary-builder.html) to mint proper names from the buildings blocks provided by the I-ADOPT ontology.
3. These terms should be mapped to the existing notations in the ObervedVariableX lists to pave the way for migration.
NB: The wmdr2_property.csv and wmdr2_object_of_interest.csv files are manually curated.
