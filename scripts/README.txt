#generate ttls and check for existence and consistency against target registry
tmode=test python -m scripts.check_urls

#reset wmdr register on test to match the content of prod 
python scripts/synchroniseTestProd.py username password 

# upload new (post) and updates (put)
python scripts/uploadChanges.py username password test '{"PUT": [],"POST": []}'
