import os

date_txt = open(os.path.join(os.path.dirname(__file__), "basic.ics"), "r", encoding="utf-8")
token = date_txt.read()
date_txt.close()

pas_filtré = token.split("\n")
filtré=[]

for didier in pas_filtré:
    if "SUMMARY" in didier or "DTSTART" in didier:
        filtré.append(didier)
    else:
        pass

string_filtré = "\n".join(filtré)

filtré_txt = open(os.path.join(os.path.dirname(__file__), "filtré.txt"), "a", encoding="utf-8")
filtré_txt.write(string_filtré)
filtré_txt.close()

date_txt = open(os.path.join(os.path.dirname(__file__), "filtré.txt"), "r", encoding="utf-8")
token = date_txt.read()
date_txt.close()

pas_filtré = token.split("\n")
filtré=[]

prout = 0

for didier in pas_filtré:
    if "2022" in didier:
        didier_2 = didier.replace("2022", "")
        filtré.append(didier_2)
        print(didier_2)
        prout += 1
    if "2023" in didier:
        didier_3 = didier.replace("2023", "")
        filtré.append(didier_3)
        print(didier_3)
        prout += 1
    if "SUMMARY" in didier:
        filtré.append(didier)
print(prout)

string_filtré = "\n".join(filtré)
string_filtré_le_vrai = string_filtré.replace("DTSTART;VALUE=DATE:", "").replace("SUMMARY:", "")


filtré_txt = open(os.path.join(os.path.dirname(__file__), "filtré_filtré.txt"), "a", encoding="utf-8")
filtré_txt.write(string_filtré_le_vrai)
filtré_txt.close()