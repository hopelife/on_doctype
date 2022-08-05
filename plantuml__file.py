# -*- coding=utf-8 -*-
"""
Implements: 
    [X] .pu file -> str
    [] 

Usages: 
    - 
"""

##@@@ Import AREA
##============================================================

##@@ Built-In Modules
##------------------------------------------------------------
# from email.headerregistry import DateHeader
import os, sys
import re

##@@ Installed Modules
##------------------------------------------------------------
from on_builtin.util_data import _file_list, _write_file

##@@ Custom Modules
##------------------------------------------------------------

# sys.path.append(os.path.join(os.path.dirname(__file__), "../api_ebest"))



#@@@ Declaration AREA
##============================================================

##@@ Static Literals / Variables
##------------------------------------------------------------


##@@ Dynamic Literals / Variables
##------------------------------------------------------------


##@@@ Definition AREA
##============================================================

##@@ Private Functions
##------------------------------------------------------------

##@@@ Execution AREA
##============================================================
if __name__ == "__main__":
    pass
    patterns = dict(
        _1_Creational = [
            "Abstract factory",
            "Builder", 
            "Factory method",
            "Prototype",
            "Singleton"
        ],
        _2_Structural = [
            "Adapter",
            "Bridge",
            "Composite",
            "Decorator",
            "Facade",
            "Flyweight",
            "Proxy"
        ],
        _3_Behavioral = [
            "Chain of Responsibility",
            "Command",
            "Interpreter",
            "Iterator",
            "Mediator",
            "Memento",
            "Observer",
            "State",
            "Strategy",
            "Template method",
            "Visitor"
        ],
    )


    stem = "template_method"
    # stem = "Visitor"

    def _rename_pattern(stem):
        for key, _patterns in patterns.items():
            for i, _pattern in enumerate(_patterns):
                if stem.lower() == _pattern.replace(" ", "_").lower():
                    return f"{key}:{str(i+1).zfill(2)}:{stem}"
    
    # print(f"{_rename_pattern(stem)=}")

    ## NOTE: PlantUMLDesignPatterns

    folder = r"C:\Dev\__pyon\on_doctype\_reference\plantuml\PlantUMLDesignPatterns"

    paths = _file_list(folder, finds=["*.txt"], recursive=False)

    names = []
    for path in paths:
        stem = path.rsplit("/", 1)[1].split(".", 1)[0]
        names.append((stem, _rename_pattern(stem)))
        # names.append({'stem': stem, 'name' :_rename_pattern(stem)})

    # names = sorted(names, key=lambda x : x['name'])
    names = sorted(names, key=lambda x : x[1])

    content = ""
    heading1 = ""
    for (stem, name) in names:
        with open(f"{folder}\\{stem}.txt", "r", encoding="utf-8") as f:
            uml = f.read()
        uml = uml.replace("@startuml", "```\n@startuml").replace("@enduml", "@enduml\n```")
        uml = re.sub(r"/'\s*[A-Z ]+'/\s*\n", "", uml)
        (category, num, _stem) = name.split(":")
        category = category.rsplit("_", 1)[1]
        if heading1 != category:
            content += f"# {category}\n\n"
            heading1 = category
        
        content += f"## {num} {_stem.replace('_', ' ').capitalize()}\n\n" + uml + "\n\n"
    
    _write_file(content, "./PlantUMLDesignPatterns.md")
    # print(content)


    ## NOTE: programmersought.com
    # folder = r"C:\Dev\__pyon\on_doctype\_reference\plantuml\programmersought.com"

    # paths = _file_list(folder, finds=["*.pu"], recursive=False)
    # paths = sorted(paths)
    # content = ""

    # for path in paths:
    #     stem = path.rsplit("/", 1)[1].split(".", 1)[0].replace("_", " ")
    #     print(stem)
    #     with open(path, "r", encoding="utf-8") as f:
    #         uml = f.read()
    #     uml = uml.replace("@startuml", "```\n@startuml").replace("@enduml", "@enduml\n```")
    #     content += f"## {stem}\n\n" + uml + "\n\n"
    
    # _write_file(content, "./programmersought.md")
    # print(content)