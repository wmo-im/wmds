The wmdr2_property_v2.csv and wmdr2_Object_of_Interest_v2.csv are properties and object of
interest (OoI) quantities which were derived from the existing wmdr code: WMO Codes
Registry: wmdr/ObservedVariableAtmosphere. The properties and OoIs were identified through
decomposition of the ObservedVariableAtmosphere variables based on the I-ADOPT framework,
variable information, e.g., “description” and “rdfs:label”.  Decomposition is subjective to
a certain degree, therefore there may be mistakes/inconsistencies or misunderstanding of the
variable.  The intent of these two files is for discussion and further revisions, while
demonstrating the I-ADOPT framework is applicable to atmospheric measurements.  There are
about a dozen variables that are not decomposed due to lack of information and understanding.

Based on the discussion at the recent I-ADOPT workshop, property constraints are used to modify
properties.  The practical guideline used here is that the property constraints shall not alter
the dimension or the nominal unit of the associated property. For example, we did not use “spectral”
as a constraint for the property “radiance” since they have different dimensions.  We also have both
“mass fraction” and “volume fraction” as they have different nominal units, i.e., kg.kg-1 vs. m-3.m3.
A more liberal definition of OoI [MOU1][GC2]was used to decompose the variables.  For example,
“Radiation” and “wind” were identified as OoI as well as both “air” and “atmosphere” are used as OoIs.
The distinction is that “atmosphere” is associated with layers, turbulence, and other thermodynamic or
dynamic processes.

