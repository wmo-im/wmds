<?xml version="1.0" encoding="UTF-8"?>
<schema xmlns="http://purl.oclc.org/dsdl/schematron" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" fpi="http://schemas.opengis.net/tsml/1.0/xsd-xml-rules.sch" see="http://www.opengis.net/spec/timeseriesml/1.0/req/xsd-xml-rules" queryBinding="xslt1">

  <!--
        This schematron schema checks the XML encoding requirements of WMDR 1.0, as specified
        in the requirements class xml-rules 
        
        version="1.0.0"
    -->
  <title>WMDR 1.0 XML Rules</title>
  <ns prefix="wmdr" uri="http://def.wmo.int/wmdr/2017"/>
  <ns prefix="om" uri="http://www.opengis.net/om/2.0"/>
  <ns prefix="gml" uri="http://www.opengis.net/gml/3.2"/>
  <ns prefix="xlink" uri="http://www.w3.org/1999/xlink"/>
  <p>This schematron schema checks aspects of the XML encoding requirements of WMDR</p>
  <pattern id="time-zone">
    <title>Test recommendation: /req/xsd-xml-rules/time-zone</title>
    <rule context="wmdr:fileDateTime">
      <!--Test rule is defined by the regular expression: (Z|[+-]HH:MM)-->
      <assert test="matches(.,'.*Z|[+-]\d{2}:\d{2}$')">The value of each wmdr:fileDateTime element shall include a time zone definition
         using a signed 4 digit character or a ‘Z’ to represent Zulu or Greenwich Mean Time (GMT).
       </assert>
    </rule>
    <rule context="gml:beginPosition">
      <!--Test rule is defined by the regular expression: (Z|[+-]HH:MM)-->
      <assert test="matches(.,'.*Z|[+-]\d{2}:\d{2}$')">The value of each gml:beginPosition element shall include a time zone definition
         using a signed 4 digit character or a ‘Z’ to represent Zulu or Greenwich Mean Time (GMT).
       </assert>
    </rule>
    <rule context="gml:endPosition">
      <!--Test rule is defined by the regular expression: (Z|[+-]HH:MM)-->
      <assert test="matches(.,'.*Z|[+-]\d{2}:\d{2}$')">The value of each gml:endPosition element shall include a time zone definition
         using a signed 4 digit character or a ‘Z’ to represent Zulu or Greenwich Mean Time (GMT).
       </assert>
    </rule>
  </pattern>
  
  <!-- the logic for sch:report is opposite to assert; you report if the statement is true -->
  <pattern id="xlink-valid-local-reference">
    <title>Test recommendation: /req/xsd-xml-rules/xlink-valid-local-reference</title>
    <rule context="*[@xlink:href]">
      <!-- removed namespace just use local namespace-uri()='http://www.opengis.net/gml/3.2' and   -->
      <report test="starts-with(@xlink:href, '#') and not(//@*[local-name()='id' ]=substring(@xlink:href, 2))">There is an issue with this xlink:href - If an xlink:href is a local reference (e.g. #abc123
        the referenced element must exist in the same document. i.e. there must be an element with gml:id="abc123" </report>
    </rule>
  </pattern>
  <!-- timeseries.sch  includes an xlink title for observed property and feature of interest -->
</schema>
