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
  <p>This schematron schema checks that the correct WMO codelists are referenced</p>
  
<!-- 1-01 Observed variable – measurand 

http://codes.wmo.int/common/wmdsObservedVariable-->

<pattern id="observed-variable">
	  <title>Assert that the correct codelist is used for om:observedProperty</title>
	  <rule context="om:observedProperty">
      <!-- check the correct codelist is used.  -->
      <assert test="starts-with(@xlink:href, 'http://codes.wmo.int/common/wmdsObservedVariable/')">The element om:observedProperty should use xlink:href to refer to an item from the codelist at http://codes.wmo.int/common/wmdsObservedVariable</assert>
	  </rule>
</pattern>

<!--1-02 Measurement unit 

http://codes.wmo.int/common/unit -->

<pattern id="measurement-unit">
	  <title>Assert that the correct codelist is used for wmdr:uom</title>
	  <rule context="wmdr:uom">
      <!-- check the correct codelist is used.  -->
      <assert test="starts-with(@xlink:href, 'http://codes.wmo.int/common/unit/')">The element wmdr:uom should use xlink:href to refer to an item from the codelist at http://codes.wmo.int/common/unit</assert>
	  </rule>
</pattern>

<!-- 1-05 Representativeness 
http://codes.wmo.int/common/wmdsRepresentativeness-->
	
<pattern id="representativeness">
	  <title>Assert that the correct codelist is used for wmdr:representativeness</title>
	  <rule context="wmdr:representativeness">
      <!-- check the correct codelist is used.  -->
      <assert test="starts-with(@xlink:href, 'http://codes.wmo.int/common/wmdsRepresentativeness/')">The element wmdr:representativeness should use xlink:href to refer to an item from the codelist at http://codes.wmo.int/common/wmdsRepresentativeness</assert>
	  </rule>
</pattern>

<!-- 2-01 Application areas 
http://codes.wmo.int/common/wmdsApplicationArea -->

<pattern id="application-area">
	  <title>Assert that the correct codelist is used for wmdr:applicationArea</title>
	  <rule context="wmdr:applicationArea">
      <!-- check the correct codelist is used.  -->
      <assert test="starts-with(@xlink:href, 'http://codes.wmo.int/common/wmdsApplicationArea/')">The element wmdr:applicationArea should use xlink:href to refer to an item from the codelist at http://codes.wmo.int/common/wmdsApplicationArea</assert>
	  </rule>
</pattern>

<!-- 2-02 Programme/Network affiliation 
http://codes.wmo.int/common/wmdsProgramAffiliation-->

<pattern id="program-affiliation">
	  <title>Assert that the correct codelist is used for wmdr:programAffiliation</title>
	  <rule context="wmdr:programAffiliation">
      <!-- check the correct codelist is used.  -->
      <assert test="starts-with(@xlink:href, 'http://codes.wmo.int/common/wmdsProgramAffiliation/')">The element wmdr:programAffiliation should use xlink:href to refer to an item from the codelist at http://codes.wmo.int/common/wmdsProgramAffiliation</assert>
	  </rule>
</pattern>

<!-- 3-01 Region of origin of data 
http://codes.wmo.int/common/wmdsWMORegion-->
	

<pattern id="wmo-region">
	  <title>Assert that the correct codelist is used for wmdr:wmoRegion</title>
	  <rule context="wmdr:wmoRegion">
      <!-- check the correct codelist is used.  -->
      <assert test="starts-with(@xlink:href, 'http://codes.wmo.int/common/wmdsWMORegion/')">The element wmdr:wmoRegion should use xlink:href to refer to an item from the codelist at http://codes.wmo.int/common/wmdsWMORegion</assert>
	  </rule>
</pattern>

<!-- 3-02 Territory of origin of data 
http://codes.wmo.int/common/wmdsTerritoryName-->
	

<pattern id="territory-name">
	  <title>Assert that the correct codelist is used for wmdr:territoryName</title>
	  <rule context="wmdr:territoryName">
      <!-- check the correct codelist is used.  -->
      <assert test="starts-with(@xlink:href, 'http://codes.wmo.int/common/wmdsTerritoryName/')">The element wmdr:territoryName should use xlink:href to refer to an item from the codelist at http://codes.wmo.int/common/wmdsTerritoryName</assert>
	  </rule>
  </pattern>

<!-- 3-04 Station/platform type 
http://codes.wmo.int/common/wmdsFacilityType-->
	

<pattern id="facility-type">
	  <title>Assert that the correct codelist is used for wmdr:facilityType</title>
	  <rule context="wmdr:facilityType">
      <!-- check the correct codelist is used.  -->
      <assert test="starts-with(@xlink:href, 'http://codes.wmo.int/common/wmdsFacilityType/')">The element wmdr:facilityType should use xlink:href to refer to an item from the codelist at http://codes.wmo.int/common/wmdsFacilityType</assert>
	  </rule>
</pattern>

<!-- 3-08 Data communication method 
http://codes.wmo.int/common/wmdsDataCommunicationMethod-->
	
<pattern id="communication-method">
	  <title>Assert that the correct codelist is used for wmdr:communicationMethod</title>
	  <rule context="wmdr:communicationMethod">
      <!-- check the correct codelist is used.  -->
      <assert test="starts-with(@xlink:href, 'http://codes.wmo.int/common/wmdsDataCommunicationMethod/')">The element wmdr:communicationMethod should use xlink:href to refer to an item from the codelist at http://codes.wmo.int/common/wmdsDataCommunicationMethod</assert>
	  </rule>
</pattern>

<!-- 3-09 Station/Platform operating status 
http://codes.wmo.int/common/wmdsReportingStatus-->
	

<pattern id="reporting-status">
	  <title>Assert that the correct codelist is used for wmdr:reportingStatus</title>
	  <rule context="wmdr:reportingStatus">
      <!-- check the correct codelist is used.  -->
      <assert test="starts-with(@xlink:href, 'http://codes.wmo.int/common/wmdsReportingStatus/')">The element wmdr:reportingStatus should use xlink:href to refer to an item from the codelist at http://codes.wmo.int/common/wmdsReportingStatus</assert>
	  </rule>
</pattern>


<!-- ************************* TO DO - multiple surface cover lists **********************************-->
<!-- 4-01

Surface cover types (UMD) -->
	


<pattern id="surface-cover">
	  <title>Assert that one of the correct codelists is used for wmdr:surfaceCover</title>
	  <rule context="wmdr:surfaceCover">
      <!-- check one of the correct codelists is used.  -->
      <assert test="starts-with(@xlink:href, 'http://codes.wmo.int/common/wmdsSurfaceCoverIGBP/') or starts-with(@xlink:href, 'http://codes.wmo.int/common/wmdsSurfaceCoverUMD/') or starts-with(@xlink:href, 'http://codes.wmo.int/common/wmdsSurfaceCoverLAI/') or starts-with(@xlink:href, 'http://codes.wmo.int/common/wmdsSurfaceCoverNPP/') or starts-with(@xlink:href, 'http://codes.wmo.int/common/wmdsSurfaceCoverPFT/') or starts-with(@xlink:href, 'http://codes.wmo.int/common/wmdsSurfaceCoverLCCS/')">The element wmdr:surfaceCover should use xlink:href to refer to an item from one of the codelists at: http://codes.wmo.int/common/wmdsSurfaceCoverIGBP, http://codes.wmo.int/common/wmdsSurfaceCoverUMD, http://codes.wmo.int/common/wmdsSurfaceCoverLAI, http://codes.wmo.int/common/wmdsSurfaceCoverNPP, http://codes.wmo.int/common/wmdsSurfaceCoverPFT, http://codes.wmo.int/common/wmdsSurfaceCoverLCCS</assert>
	  </rule>
</pattern>



<!-- 4-02 Surface cover classification scheme 
http://codes.wmo.int/common/wmdsSurfaceCoverClassification-->
	

<pattern id="surface-cover-classification">
	  <title>Assert that the correct codelist is used for wmdr:surfaceCoverClassification</title>
	  <rule context="wmdr:surfaceCoverClassification">
      <!-- check the correct codelist is used.  -->
      <assert test="starts-with(@xlink:href, 'http://codes.wmo.int/common/wmdsSurfaceCoverClassification/')">The element wmdr:surfaceCoverClassification should use xlink:href to refer to an item from the codelist at http://codes.wmo.int/common/wmdsSurfaceCoverClassification</assert>
	  </rule>
</pattern>

<!-- 4-03-01 Local topography 
http://codes.wmo.int/common/wmdsLocalTopography-->
	

<pattern id="local-topography">
	  <title>Assert that the correct codelist is used for wmdr:localTopography</title>
	  <rule context="wmdr:localTopography">
      <!-- check the correct codelist is used.  -->
      <assert test="starts-with(@xlink:href, 'http://codes.wmo.int/common/wmdsLocalTopography/')">The element wmdr:localTopography should use xlink:href to refer to an item from the codelist at http://codes.wmo.int/common/wmdsLocalTopography</assert>
	  </rule>
</pattern>

<!-- 4-03-02 Relative elevation 
http://codes.wmo.int/common/wmdsRelativeElevation-->
	

<pattern id="relative-elevation">
	  <title>Assert that the correct codelist is used for wmdr:relativeElevation</title>
	  <rule context="wmdr:relativeElevation">
      <!-- check the correct codelist is used.  -->
      <assert test="starts-with(@xlink:href, 'http://codes.wmo.int/common/wmdsRelativeElevation/')">The element wmdr:relativeElevation should use xlink:href to refer to an item from the codelist at http://codes.wmo.int/common/wmdsRelativeElevation</assert>
	  </rule>
</pattern>

<!-- 4-03-03 Topographic context 
http://codes.wmo.int/common/wmdsTopographicContext-->
	


<pattern id="topographic-context">
	  <title>Assert that the correct codelist is used for wmdr:topographicContext</title>
	  <rule context="wmdr:topographicContext">
      <!-- check the correct codelist is used.  -->
      <assert test="starts-with(@xlink:href, 'http://codes.wmo.int/common/wmdsTopographicContext/')">The element wmdr:topographicContext should use xlink:href to refer to an item from the codelist at http://codes.wmo.int/common/wmdsTopographicContext</assert>
	  </rule>
</pattern>

<!-- 4-03-04 Altitude/depth 

http://codes.wmo.int/common/wmdsAltitudeOrDepth-->
	

<pattern id="altitude-or-depth">
	  <title>Assert that the correct codelist is used for wmdr:altitudeOrDepth</title>
	  <rule context="wmdr:altitudeOrDepth">
      <!-- check the correct codelist is used.  -->
      <assert test="starts-with(@xlink:href, 'http://codes.wmo.int/common/wmdsAltitudeOrDepth/')">The element wmdr:altitudeOrDepth should use xlink:href to refer to an item from the codelist at http://codes.wmo.int/common/wmdr/wmdrAltitudeOrDepth</assert>
	  </rule>
</pattern>

<!-- 4-04
	TO DO
Events at station/platform -->
	
<!--
http://codes.wmo.int/common/wmdsEventAtFacility
<pattern id="altitude-or-depth">
	  <title>Assert that the correct codelist is used for altitudeOrDepth</title>
	  <rule context="wmdr:altitudeOrDepth"> -->
      <!-- check the correct codelist is used.  -->
   <!--   <assert test="starts-with(@xlink:href, 'http://codes.wmo.int/common/wmdr/wmdrAltitudeOrDepth')">The element altitudeOrDepth should use xlink:href to refer to an item from the codelist at http://codes.wmo.int/common/wmdr/wmdrAltitudeOrDepth</assert>
	  </rule>
</pattern>
-->


<!-- 4-06
Surface Roughness (Davenport roughness classification) 

http://codes.wmo.int/common/wmdsSurfaceRoughnessDavenport-->
	

<pattern id="surface-roughness">
	  <title>Assert that the correct codelist is used for wmdr:surfaceRoughness</title>
	  <rule context="wmdr:surfaceRoughness">
      <!-- check the correct codelist is used.  -->
      <assert test="starts-with(@xlink:href, 'http://codes.wmo.int/common/wmdsSurfaceRoughnessDavenport/')">The element wmdr:surfaceRoughness should use xlink:href to refer to an item from the codelist at http://codes.wmo.int/common/wmdsSurfaceRoughnessDavenport</assert>
	  </rule>
</pattern>

<!-- 4-07
	

Climate Zone
	

http://codes.wmo.int/common/wmdsClimateZone -->
<pattern id="climate-zone">
	  <title>Assert that the correct codelist is used for wmdr:climateZone</title>
	  <rule context="wmdr:climateZone">
      <!-- check the correct codelist is used.  -->
      <assert test="starts-with(@xlink:href, 'http://codes.wmo.int/common/wmdsClimateZone/')">The element wmdr:climateZone should use xlink:href to refer to an item from the codelist at http://codes.wmo.int/common/wmdsClimateZone</assert>
	  </rule>
</pattern>

<!-- 5-01
	

Source of observation
	

http://codes.wmo.int/common/wmdsSourceOfObservation -->
<pattern id="source-of-observation">
	  <title>Assert that the correct codelist is used for wmdr:sourceOfObservation</title>
	  <rule context="wmdr:sourceOfObservation">
      <!-- check the correct codelist is used.  -->
      <assert test="starts-with(@xlink:href, 'http://codes.wmo.int/common/wmdsSourceOfObservation/')">The element wmdr:sourceOfObservation should use xlink:href to refer to an item from the codelist at http://codes.wmo.int/common/wmdsSourceOfObservation</assert>
	  </rule>
</pattern>

<!-- 5-02
	

Measurement/observing method
	

http://codes.wmo.int/common/wmdsObservingMethod -->
<pattern id="observing-method">
	  <title>Assert that the correct codelist is used for wmdr:observingMethod</title>
	  <rule context="wmdr:observingMethod">
      <!-- check the correct codelist is used.  -->
      <assert test="starts-with(@xlink:href, 'http://codes.wmo.int/common/wmdsObservingMethod/')">The element wmdr:observingMethod should use xlink:href to refer to an item from the codelist at http://codes.wmo.int/common/wmdsObservingMethod</assert>
	  </rule>
</pattern>

<!-- 5-04
	

Instrument operating status 
http://codes.wmo.int/common/wmdsInstrumentOperatingStatus-->
	


<pattern id="instrument-operating-status">
	  <title>Assert that the correct codelist is used for wmdr:instrumentOperatingStatus</title>
	  <rule context="wmdr:instrumentOperatingStatus">
      <!-- check the correct codelist is used.  -->
      <assert test="starts-with(@xlink:href, 'http://codes.wmo.int/common/wmdsInstrumentOperatingStatus/')">The element wmdr:instrumentOperatingStatus should use xlink:href to refer to an item from the codelist at http://codes.wmo.int/common/wmdsInstrumentOperatingStatus</assert>
	  </rule>
</pattern>

<!-- 5-08-01
	

Control standard type 

http://codes.wmo.int/common/wmdsControlStandardType-->
	

<pattern id="control-standard-type">
	  <title>Assert that the correct codelist is used for wmdr:standardType</title>
	  <rule context="wmdr:standardType">
      <!-- check the correct codelist is used.  -->
      <assert test="starts-with(@xlink:href, 'http://codes.wmo.int/common/wmdsControlStandardType/')">The element wmdr:standardType should use xlink:href to refer to an item from the codelist at http://codes.wmo.int/common/wmdsControlStandardType</assert>
	  </rule>
</pattern>

<!-- 5-08-02
	

Control location   
http://codes.wmo.int/common/wmdsControlLocation         -->
	

<pattern id="control-check-location">
	  <title>Assert that the correct codelist is used for wmdr:checkLocation</title>
	  <rule context="wmdr:checkLocation">
      <!-- check the correct codelist is used.  -->
      <assert test="starts-with(@xlink:href, 'http://codes.wmo.int/common/wmdsControlLocation/')">The element wmdr:checkLocation should use xlink:href to refer to an item from the codelist at http://codes.wmo.int/common/wmdsControlLocation </assert>
	  </rule>
</pattern>

<!-- 5-08-03
	

Instrument control result  http://codes.wmo.int/common/wmdsInstrumentControlResult   -->
<pattern id="control-check-result">
	  <title>Assert that the correct codelist is used for wmdr:controlCheckResult</title>
	  <rule context="wmdr:controlCheckResult">
      <!-- check the correct codelist is used.  -->
      <assert test="starts-with(@xlink:href, 'http://codes.wmo.int/common/wmdsInstrumentControlResult/')">The element wmdr:controlCheckResult should use xlink:href to refer to an item from the codelist at http://codes.wmo.int/common/wmdsInstrumentControlResult </assert>
	  </rule>
</pattern>
	



<!-- 5-14
	

Status of observation 
http://codes.wmo.int/common/wmdsInstrumentOperatingStatus-->
	

<pattern id="instrument-operating-status">
	  <title>Assert that the correct codelist is used for wmdr:instrumentOperatingStatus</title>
	  <rule context="wmdr:instrumentOperatingStatus">
      <!-- check the correct codelist is used.  -->
      <assert test="starts-with(@xlink:href, 'http://codes.wmo.int/common/wmdsInstrumentOperatingStatus/')">The element wmdr:insrtumentOperatingStatus should use xlink:href to refer to an item from the codelist at http://codes.wmo.int/common/wmdsInstrumentOperatingStatus</assert>
	  </rule>
</pattern>

<!-- 5-15
	

Exposure of instrument
	

http://codes.wmo.int/common/wmdsExposure -->
<pattern id="exposure">
	  <title>Assert that the correct codelist is used for wmdr:exposure</title>
	  <rule context="wmdr:exposure">
      <!-- check the correct codelist is used.  -->
      <assert test="starts-with(@xlink:href,'http://codes.wmo.int/common/wmdsExposure/')">The element wmdr:exposure should use xlink:href to refer to an item from the codelist at http://codes.wmo.int/common/wmdsExposure</assert>
	  </rule>
</pattern>
<!-- 6-03
	

Sampling strategy
	

http://codes.wmo.int/common/wmdsSamplingStrategy -->
<pattern id="sampling-strategy">
	  <title>Assert that the correct codelist is used for wmdr:samplingStrategy</title>
	  <rule context="wmdr:samplingStrategy">
      <!-- check the correct codelist is used.  -->
      <assert test="starts-with(@xlink:href, 'http://codes.wmo.int/common/wmdsSamplingStrategy/')">The element wmdr:samplingStrategy should use xlink:href to refer to an item from the codelist at http://codes.wmo.int/common/wmdsSamplingStrategy</assert>
	  </rule>
</pattern>

<!-- 7-06
	

Level of data
	

http://codes.wmo.int/common/wmdsLevelOfData -->
<pattern id="level-of-data">
	  <title>Assert that the correct codelist is used for wmdr:levelOfData</title>
	  <rule context="wmdr:levelOfData">
      <!-- check the correct codelist is used.  -->
      <assert test="starts-with(@xlink:href, 'http://codes.wmo.int/common/wmdsLevelOfData/')">The element wmdr:levelOfData should use xlink:href to refer to an item from the codelist at http://codes.wmo.int/common/wmdsLevelOfData</assert>
	  </rule>
</pattern>

<!-- 7-07
	

Data format
	

http://codes.wmo.int/common/wmdsDataFormat -->
<pattern id="data-format">
	  <title>Assert that the correct codelist is used for wmdr:dataFormat</title>
	  <rule context="wmdr:dataFormat">
      <!-- check the correct codelist is used.  -->
      <assert test="starts-with(@xlink:href, 'http://codes.wmo.int/common/wmds/DataFormat/')">The element wmdr:dataFormat should use xlink:href to refer to an item from the codelist at http://codes.wmo.int/common/wmdsDataFormat</assert>
	  </rule>
</pattern>

<!-- 7-10
	

Reference time
	

http://codes.wmo.int/common/wmdsReferenceTime -->
<pattern id="reference-time">
	  <title>Assert that the correct codelist is used for wmdr:referenceTime</title>
	  <rule context="wmdr:reference-time">
      <!-- check the correct codelist is used.  -->
      <assert test="starts-with(@xlink:href, 'http://codes.wmo.int/common/wmdsReferenceTime/')">The element wmdr:referenceTime should use xlink:href to refer to an item from the codelist at http://codes.wmo.int/common/wmdsReferenceTime</assert>
	  </rule>
</pattern>


<!-- TO DO 8-03 - different quality flag lists -->


<!-- 8-05
	

Traceability
	

http://codes.wmo.int/common/wmdsTraceability -->
<!--<pattern id="altitude-or-depth">
	  <title>Assert that the correct codelist is used for altitudeOrDepth</title>
	  <rule context="wmdr:altitudeOrDepth">-->
      <!-- check the correct codelist is used.  -->
    <!--  <assert test="starts-with(@xlink:href, 'http://codes.wmo.int/common/wmdr/wmdrAltitudeOrDepth')">The element altitudeOrDepth should use xlink:href to refer to an item from the codelist at http://codes.wmo.int/common/wmdr/wmdrAltitudeOrDepth</assert>
	  </rule>
</pattern> -->

<!-- 9-02
	

Data policy/use constraints
	

http://codes.wmo.int/common/wmdsDataPolicy -->
<pattern id="data-use-constraints">
	  <title>Assert that the correct codelist is used for wmdr:dataUseConstraints</title>
	  <rule context="wmdr:dataUseConstraints">
      <!-- check the correct codelist is used.  -->
      <assert test="starts-with(@xlink:href, 'http://codes.wmo.int/common/wmdsDataPolicy/')">The element wmdr:dataUseConstraints should use xlink:href to refer to an item from the codelist at http://codes.wmo.int/common/wmdsDataPolicy</assert>
	  </rule>
</pattern>

<!-- 11-01
	

Coordinates source/service
	

http://codes.wmo.int/common/wmdsGeopositioningMethod -->
<pattern id="geopositioning-method">
	  <title>Assert that the correct codelist is used for wmdr:geopositioningMethod</title>
	  <rule context="wmdr:geopositioningMethod">
      <!-- check the correct codelist is used.  -->
      <assert test="starts-with(@xlink:href, 'http://codes.wmo.int/common/wmdsGeopositioningMethod/')">The element wmdr:geopositioningMethod should use xlink:href to refer to an item from the codelist at http://codes.wmo.int/common/wmdsGeopositioningMethod</assert>
	  </rule>
</pattern>

<!-- 11-02
	

Coordinates reference
	

http://codes.wmo.int/common/wmdsCoordinateReferenceSystem -->
<pattern id="coordinate-reference-system">
	  <title>Assert that the correct codelist is used for gml:srsName</title>
	  <rule context="gml:pos">
      <!-- check on of the correct codelists is used.  -->
      <assert test="starts-with(@srsName, 'http://codes.wmo.int/common/wmdr/wmdsCoordinateReferenceSystem/') or starts-with(@srsName, 'http://www.opengis.net/def/crs/EPSG/')">The element gml:srsName should use xlink:href to refer to an item from one of the codelists at http://codes.wmo.int/common/wmdsCoordinateReferenceSystem or http://www.opengis.net/def/crs/EPSG/</assert>
	  </rule>
</pattern>

<!-- 11-03
	

Meaning of time stamp
	

http://codes.wmo.int/common/wmdsTimeStampMeaning -->
<pattern id="time-stamp-meaning">
	  <title>Assert that the correct codelist is used for wmdr:temporalReportingTimeStampMeaning</title>
	  <rule context="wmdr:temporalReportingTimeStampMeaning">
      <!-- check the correct codelist is used.  -->
      <assert test="starts-with(@xlink:href, 'http://codes.wmo.int/common/wmdsTimeStampMeaning/')">The element wmdr:temporalReportingTimeStampMeaning should use xlink:href to refer to an item from the codelist at http://codes.wmo.int/common/wmdsTimeStampMeaning</assert>
	  </rule>
</pattern>

  
</schema>
