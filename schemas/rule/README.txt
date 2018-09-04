The schematron rules provide an additional level of validation of WMDR XML content beyond that which is supported by the XSD.

Several tools can run schematron (e.g. OxygenXML, Saxon, Probatron).

Probatron (https://code.google.com/archive/p/probatron4j/) is re-distributed under the GPL (see notices in Probatron zip file).

This program is a Java Jar executable which can be used to run schematron as follows:

java -jar probatron.jar -r1 [pathToXMLFileToTest.xml] [pathToSchematronToRun.sch]

The schematron are as follows:

xml-valid.sch  - tests aspects of the XML encoding such as times and local references.
observation.sch - tests that O&M is used appropriately for WMDR.
codelists.sch - tests that the appropriate WMDR codelists are used.

