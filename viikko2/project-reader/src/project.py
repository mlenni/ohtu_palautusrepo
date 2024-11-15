class Project:
    def __init__(self, name, description, license, authors, dependencies, dev_dependencies):
        self.name = name
        self.description = description
        self.license = license
        self.authors = authors
        self.dependencies = dependencies
        self.dev_dependencies = dev_dependencies

    def _stringify_dependencies(self, dependencies):
        return ", ".join(dependencies) if len(dependencies) > 0 else "-"

    def _stringify_list(self, items):
        return "\n".join(f"- {item}" for item in items) if items else "-"
    
    def __str__(self):
        return (
        f"Name: {self.name}\n"
        f"Description: {self.description or '-'}\n"
        f"License: {self.license or '-'}\n\n"
        f"Authors:\n{self._stringify_list(self.authors)}\n\n"
        f"Dependencies:\n{self._stringify_list(self.dependencies)}\n\n"
        f"Development dependencies:\n{self._stringify_list(self.dev_dependencies)}"
        )
