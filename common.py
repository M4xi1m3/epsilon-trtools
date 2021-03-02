
import glob
import csv
import re

def load_i18n(path):
    # Read data from i18n files
    files = glob.glob(path + ".*.i18n")

    if len(files) == 0:
        return None, None

    data = {}
    langs = []

    for p in files:
        lang = re.search("\\.(.+)\\.i18n$", p).group(1)
        langs.append(lang)

        with open(p, "r") as f:
            for l in f:
                r = re.search("^([A-Za-z0-9_]+)\\s*=\\s*\"(.*)\"$", l).groups()

                if not r[0] in data:
                    data[r[0]] = {}

                data[r[0]][lang] = r[1]
    return data, langs

def load_csv(path):
    data = {}
    
    with open(path, "r") as f:
        reader = csv.reader(f, delimiter=';', quotechar='"', lineterminator='\n', quoting=csv.QUOTE_ALL)
        langs = list(next(reader)[1:])
        for line in reader:
            data[line[0]] = {}
            
            for i in range(0, len(line[1:])):
                data[line[0]][langs[i]] = line[1:][i]
    
    return data, langs

def clean_data(data, langs):
    # Remove empty string values (important when loading CSV)
    for key in data:
        for l in langs:
            if l in data[key]:
                if data[key][l] == "":
                    del data[key][l]

    # See if non-universals can be made universals
    if "universal" in langs:
        for key in data:
            val = data[key]
            
            if not "universal" in val:
                tmp = ""
                for l in langs:
                    if l in val:
                        tmp = val[l]
                if all(value == tmp for value in val.values()):
                    val = data[key] = {"universal": tmp}

    return data, langs

def save_csv(path, data, langs):
    # Write data to csv
    with open(path, "w") as f:
        writer = csv.writer(f, delimiter=';', quotechar='"', lineterminator='\n', quoting=csv.QUOTE_ALL)
        
        first_row = ["key"]
        first_row.extend(langs)
        writer.writerow(first_row)
        
        for key in data:
            row = [key]
            
            for l in langs:
                if l in data[key]:
                    row.append(data[key][l])
                else:
                    row.append("")
            writer.writerow(row)

def save_i18n(path, data, langs):
    for l in langs:
        with open(path + "." + l + ".i18n", "w") as f:
            for k in data:
                if l in data[k]:
                    f.write(k + " = \"" + data[k][l] + "\"\n")

