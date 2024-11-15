from urllib import request
from project import Project
import tomli

class ProjectReader:
    def __init__(self, url):
        self._url = url

    def get_project(self):
        # tiedoston merkkijonomuotoinen sisältö
        content = request.urlopen(self._url).read().decode("utf-8")
        # print(content)
        
        # deserialisoi TOML-formaatissa oleva merkkijono ja muodosta Project-olio sen tietojen perusteella
        toml_content = tomli.loads(content)
        
        name = toml_content.get("tool", {}).get("poetry", {}).get("name", "Unknown name")
        description = toml_content.get("tool", {}).get("poetry", {}).get("description", "No description")
        license = toml_content.get("tool", {}).get("poetry", {}).get("license", "No license")
        authors = toml_content.get("tool", {}).get("poetry", {}).get("authors", [])
        dependencies = list(toml_content.get("tool", {}).get("poetry", {}).get("dependencies", {}).keys())
        dev_dependencies = list(toml_content.get("tool", {}).get("poetry", {}).get("group", {}).get("dev", {}).get("dependencies", {}).keys())
        return Project(name, description, license, authors, dependencies, dev_dependencies)
