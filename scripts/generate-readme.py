from registry_deployment import createReadme


with open(r"tables/readme.md","w",encoding="utf8") as f:
    f.write(createReadme())
