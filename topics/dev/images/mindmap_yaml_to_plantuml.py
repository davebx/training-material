import os
import sys
import yaml


def main():
    for arg in sys.argv[1:]:
        arg_name = os.path.basename(arg)
        with open(arg, "r") as f:
            mindmap = yaml.safe_load(f)

        lines = [
            '@startmindmap',
            '!include plantuml_style.txt',
            '!include plantuml_options.txt',
            "' DO NOT EDIT: auto-generated from %s" % os.path.basename(arg_name),
        ]

        def append_lines(mindmap_dict, indent=1):
            line = "*" * indent + ""
            if isinstance(mindmap_dict, dict):
                label = mindmap_dict["label"]
                doc = mindmap_dict.get("doc")
                items = mindmap_dict.get("items", [])
            else:
                label = mindmap_dict
                doc = None
                items = []

            if doc:
                line += ":<b><i>" + label + "</i></b>\n " + doc + ";"
            else:
                line += " <b><i>" + label + "</i></b>"

            lines.append(line)
            for item in items:
                append_lines(item, indent + 1)
        
        append_lines(mindmap)
        lines.append("@endmindmap")
        plantuml_path = arg_name[0:-len("mindmap.yml")] + "plantuml.txt"
        with open(plantuml_path, "w") as f:
            f.write("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
