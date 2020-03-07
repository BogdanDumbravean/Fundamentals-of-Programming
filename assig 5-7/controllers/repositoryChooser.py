from domain.repository import *
import sys

class RepositoryChooser:
    def readSettings(self):
        settings = {}
        f = open(sys.path[0] + "\\settings.properties", "r")
        s = f.read()
        lines = s.split('\n')
        for line in lines:
            tokens = line.split('=')
            settings[tokens[0].strip()] = tokens[1].strip()
        f.close()
        return settings

    def chooseRepository(self, item, file):
        settings = self.readSettings() 
        if settings["repo_type"] == "memory":
            return Repository()
        elif settings["repo_type"] == "text":
            return TextFileRepository(item, settings[file])
        elif settings["repo_type"] == "binary":
            return PickleFileRepository(item, settings[file])
        elif settings["repo_type"] == "json":
            return JsonFileRepository(item, settings[file]) 
        elif settings["repo_type"] == "sql":
            return SqlFileRepository(item, settings[file])  