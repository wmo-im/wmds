<?xml version="1.0" encoding="UTF-8"?>
<schema xmlns="http://purl.oclc.org/dsdl/schematron" queryBinding="xslt1" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <!--
        This Schematron schema checks that the correct feature types are used for the properties of OM_Observation.
    
        version="1.0.0" 
    -->
  <title>WMDR Feature of Interest Check</title>
  <p>Verifies that the om:featureOfInterest element is a SpatialSamplingFeature.</p>
  <ns prefix="wmdr" uri="http://def.wmo.int/wmdr/2017"/>
  <ns prefix="om" uri="http://www.opengis.net/om/2.0"/>
  <ns prefix="sams" uri="http://www.opengis.net/samplingSpatial/2.0"/>

  <pattern id="featureOfInterest">
    <title>Test requirement: /req/observation/observation-feature-of-interest</title>
    <rule context="om:OM_Observation/om:featureOfInterest">
      <assert test="sams:SF_SpatialSamplingFeature">The xml element om:featureOfInterest shall contain a SF_SpatialSamplingFeature.</assert>           
    </rule>
  </pattern>
  
  <pattern id="result">
    <title>Test requirement: /req/observation/observation-result</title>
    <rule context="om:OM_Observation/om:result">
      <assert test="wmdr:ResultSet">The xml element om:result shall contain a wmdr ResultSet.</assert>           
    </rule>
  </pattern>
  
  <pattern id="process">
    <title>Test requirement: /req/observation/observation-process</title>
    <rule context="om:OM_Observation/om:procedure">
      <assert test="wmdr:Process">The xml element om:process shall contain a wmdr Process.</assert>           
    </rule>
  </pattern>

</schema>
