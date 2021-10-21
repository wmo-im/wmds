## Testing and management

scripts provides tools written in Python to check content consistency with the published test and prod registers and to upload changes.

example usage:

* generate `ttl` files and check for existence and consistency against target registry

```
tmode=test python -m scripts.check_urls
```

* generate `ttl` files and check for existence and consistency against target registry, sending outputs for upload to a named local file 

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


* reset wmdr register on test to match the content of prod 

```
python scripts/synchroniseTestProd.py username password 
```

