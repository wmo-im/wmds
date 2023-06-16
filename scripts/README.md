## Workflows
There are two github workflows configured for this repository.

### Generate TTL and commit
The generateTTLandCommit.yml runs on the pull request.  It creates all `ttl` files from the csv source, then uses git to evaluate which files have changed content.  Any files which have changed are then placed into a new github action commit and added to the pull request for review.

### Check consistency
The check_consistency.yml runs only when a pull request is merged or the master branch is changed directly. This checks that the contents on the 'test' and 'prod' registers is consistent with the repository. It is expected to fail when the codes are amended and have not been uploaded to the registry. The tests can be rerun following managed upload through the github actions tab.

## Testing and management
These scripts provides tools written in Python to check content consistency with the published test and prod registers and to upload changes.

* reset wmdr register on test to match the content of prod 

```
python scripts/synchroniseTestProd.py username password 
```

* generate `ttl` files 
```
tmode=test python3 -m scripts.makeWMDREntities
```
 
* check for existence and consistency against target registry
```
tmode=test python3 -m scripts.check_urls
```

* check for existence and consistency against target registry and send outputs for upload to a named local file 

```
tmode=test outfile=</path/to/writeable/file> python3 -m scripts.check_urls
```

* upload new (post) and updates (put) (using JSON encoded text input at the command line)

```
python scripts/uploadChanges.py username password test '{"PUT": [],"POST": []}'
```

* upload new (post) and updates (put) (using JSON encoded local file input)

```
python3 -m scripts.uploadChanges <uname> <temporaryKey> test </path/to/a/readable/file>
```



