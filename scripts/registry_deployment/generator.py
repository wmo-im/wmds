import csv
import io
import os
import re
import tempfile
import sys, traceback
import logging
import unicodedata
import datetime

from string import Template 

logging.getLogger(__name__).addHandler(logging.NullHandler())
logger = logging.getLogger()


TABLES_DIR = "./tables_en"

header_tpl = Template("""@prefix dct:   <http://purl.org/dc/terms/> .
@prefix rdf:   <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs:  <http://www.w3.org/2000/01/rdf-schema#> .
@prefix skos:  <http://www.w3.org/2004/02/skos/core#> .
@prefix ldp:   <http://www.w3.org/ns/ldp#> .
@prefix reg:   <http://purl.org/linked-data/registry#> .
@prefix xsd:   <http://www.w3.org/2001/XMLSchema#> .
@prefix owl:   <http://www.w3.org/2002/07/owl#> .
""")

item_tpl = Template("""<$container/$notation>
    a                skos:Concept ;
    rdfs:label       "$label" ;
    dct:description  "$description"@en ;
    skos:notation    "$notation" .
    
    """)
    
collection_tpl = Template("""<$container>
    a                      skos:Collection  ;
    rdfs:label             "$description" ;
    dct:description        "WMO $description" ;
    skos:member            $members .
    """)

class Codelist:

    def __init__(self,code_nr,name,url):
    
        self.code_nr=code_nr
        self.url=url
        self.name=name


    def __str__(self):
        return "{code_nr} {url} {name}".format(**self.__dict__)

def notPrintable(text):
    
    cnt=1
    for c in text:
        
        if unicodedata.category(c)[0]=="C":
            utfval = "{:02x}".format(ord(c))
            print("problem character:{} at {}".format(utfval,cnt))
            return True
        cnt+=1
    
    return False

def testEntry(notation,label,description):

  
    if notPrintable(description):
        raise ValueError("ERROR unprintable character in definition {}".format(d[definitionStr])) 
    
    if notPrintable(label):
        raise ValueError("ERROR unprintable character in label ".format(label)) 
                      
    
    # check notation
    
    allowed = r"^[A-Za-z0-9_.\-~$+!*'(),]+$"
    
    if not re.match(allowed,notation):
        raise ValueError("invalid characer in '{}'".format(notation))
    
    if notation[0] == "_" :
        raise ValueError("notation '{}' cannot start with _".format(notation))
    
    try:
        notation.encode('latin1')
    except UnicodeEncodeError as ue:
        raise ValueError("notation '{}' contains non-latin1 characters".format(notation))




def processCodelist(c,dir=None):

    filename = "{}.csv".format(c.code_nr)
    filepath = r"{}/{}".format(TABLES_DIR,filename)
       
    logger.debug("processFile: {} , {}".format(c.code_nr,filepath))
        
    codelistLabel = c.name
    codelistDescription = c.name

       
    codelist_nr = c.code_nr
    
    #if codelist_nr in ['1-01-01','1-01-02','1-01-03','1-01-04','1-01-05']:
    #    print("skipping {}".format(codelist_nr))
    #    return

      
    base_description = c.name
    name = c.name
    
    notationStr = 'notation'
    descriptionStr = 'description'
    labelStr = 'name'
    
        
    with open(filepath, mode='rb' ) as f:
        
        if dir and os.path.isdir(dir):
            ttlfile = open( "{}/{}.ttl".format( dir,c.code_nr ) , mode="w" , encoding="utf-8" )
        else :
            ttlfile = tempfile.TemporaryFile(mode="w",encoding="utf-8")
        
        data = f.read()
        
        # try to encode in latin1.. this throws an error which is caught outside
        data.decode('latin1')
        
        ttlfilecsvreader = csv.reader( data.decode('utf-8').splitlines() ,  delimiter=',', quotechar='"' )  

        members = [] # accumulate the members of the collection
        first = 1
        count = 0
        strbuffer=""
        for row in ttlfilecsvreader:
            count += 1
            if first:
                keys = row
                first = 0
            else:
                row = [rr.replace("\"", "\'") for rr in row]
                d = dict(zip(keys, row))
                #print(d)
                if not notationStr in d or d[notationStr] == 'NA':
                    print("ERROR notation not defined in line %d" % (count))
                    print(d)
                    sys.exit(1)
                    continue
                
                notation = d[notationStr].strip()
                description = d[descriptionStr].strip()
                label = d[labelStr].strip()
               
                member = "{}/{}".format(base_name,notation)
            
                if member in members:                   
                    raise ValueError("Two registers with the same notation: "+notation)
                
                testEntry(notation,label,description)
                
                members.append(member)
                
                strbuffer += item_tpl.substitute( container=base_name , notation=notation , description=description , label=label )
                strbuffer += "\n"
                
                #print('<' + codelist + '> a ' + type + ' ;' , file=ttlfile) #TODO
                
        now_iso = datetime.datetime.now().isoformat()
        members_str = " , ".join([ "<{}>".format(m) for m in members ])
        
        ttlfile.write( header_tpl.substitute() + "\n"  )
        ttlfile.write( collection_tpl.substitute( container=base_name , description=base_description , label=base_name, members=members_str   ) + "\n" )
        ttlfile.write( strbuffer )
    
        ttlfile.close()
    
    logger.debug("wrote {} to {}".format(codelist_nr,ttlfile.name))
    return True



    

# this function generates the TTL files from the current tables-en directory. It uses    
def generate(dir=None):    
    # get codelist to 
    codes = {}
    with open(r"{}/wmdr-tables.csv".format(TABLES_DIR),'r') as f:
        csvreader = csv.reader(f)
        
        files = []
        for line in csvreader:
            code_nr = line[0]
            name = line[1]
            url = line[2]
            
            c = Codelist(code_nr,name,url)
    
            logger.debug("processing {}".format(c))

            processCodelist(c,dir)
            logger.info("generated TTL file {}".format(c.code_nr))


        
    
# this function creates the readme file from the CSV file
def createReadme():

    # get codelist to 
    codes = {}
    with open(r"{}/wmdr-tables.csv".format(TABLES_DIR),'r',encoding="utf8") as f:
        csvreader = csv.reader(f)
        
        files = []
        temp = ""
        for line in csvreader:
            code_nr = line[0]
            name = line[1]
            url = line[2]
            abbreviation = url.split('/')[-1]
            
            temp += readme_line_tpl.substitute(number=code_nr,abbreviation=abbreviation,name=name,url=url)
            
            codes[code_nr] = url
    
    mypath = r"{}".format(TABLES_DIR)
    csvfiles = [f.replace('.csv','') for f in os.listdir( mypath ) if os.path.isfile(os.path.join(mypath, f)) and f.endswith(".csv") and "wmdr-tables" not in f ]


    missing_files = set( codes.keys() ).difference( set(csvfiles) )
    missing_in_csv = set( csvfiles ).difference( set(codes.keys()) )

    if len(missing_files)>0:
        raise ValueError("{} are referenced in wmrd-tables.csv but do not exist ".format( ",".join([ "{}.csv".format(f) for f in missing_files ] ) ))
        
    if len(missing_in_csv)>0:
        raise ValueError("{} are in filesystem but not referenced in wmrd-tables.csv ".format( ",".join( [ "{}.csv".format(f) for f in missing_in_csv ] ) ) )
        

    return str(readme_tpl.substitute(payload=temp))
            

