read_filename = "gtk.css"#input("podaj nazwę pliku do odczytania\n")
write_filename = "gtk2.css"#input("podaj nazwę pliku do zapisu\n")

with open(read_filename, "r") as file:
    content = file.readlines()

def list_to_str(l):
    ret = ""
    for i in l:
        ret += i
    return ret
def modify_rgb(l: list, r=1, g=1, b=1):
    new = l.copy()
    new[0] *= r
    new[1] *= g
    new[2] *= b
    for i in range(3):
        new[i] = int(new[i])
        if new[i] > 255:
            new[i] = 255
    return new

def index_rgba(text):
    if "rgba" in text:
        beginning = text.index("rgba")
        ending = text.index(");") +1
        return [beginning, ending]
def extract_rgba(text):
    if "rgba" in text:
        beginning = text.index("rgba")
        ending = text.index(");") +1
        return text[beginning:ending]
def rgba_to_list(rgba_string):
    ret = rgba_string[5:-1]
    ret = ret.split(", ")
    for i in range(3):
        ret[i] = int(ret[i])
    ret[3] = float(ret[3])
    return ret
def list_to_text_rgba(l):
    ret = f"rgba({str(l[0])}, {str(l[1])}, {str(l[2])}, {str(l[3])})"
    return ret
def replace_rgba(text: str, new: list):
    rgba_pos = index_rgba(text)
    new_text = list(text)
    for i in range(rgba_pos[0], rgba_pos[1]):
        new_text.pop(rgba_pos[0])
    new_text.insert(rgba_pos[0], list_to_text_rgba(new))
    return list_to_str(new_text)

def index_hex(text):
    if "#" in text:
        beginning = text.index("#")
        ending = text.index(";")
        return [beginning, ending]
def extract_hex(text):
    if "#" in text:
        return text[index_hex(text)[0]+1:index_hex(text)[1]]
def hex_to_list(hex_code):
    new_list = [hex_code[:2], hex_code[2:4], hex_code[4:]]
    new_list = [int(i, base = 16) for i in new_list]
    return new_list
def list_to_text_hex(l):
    new_list = [hex(int(i))[2:] for i in l]
    for i in range(3):
        if len(new_list[i]) == 1:
            new_list[i] = "0"+new_list[i]
        elif len(new_list[i]) == 0:
            new_list[i] = "00"
    new_list = "#" + list_to_str(new_list)
    return new_list
def replace_hex(text: str, new):
    indexes = index_hex(text)
    new_text = list(text)
    for i in range(indexes[0], indexes[1]):
        new_text.pop(indexes[0])
    new_text.insert(indexes[0], list_to_text_hex(new))
    return list_to_str(new_text)

def modify_line(text):
    newline = text
    try:
        if index_hex(text) != None:
            old_color = hex_to_list(extract_hex(text))
            new_color = modify_rgb(old_color, 1.1, 1.2, 0.9)
            newline = replace_hex(text, new_color)
        elif index_rgba(text) != None:
            old_color = rgba_to_list(extract_rgba(text))
            new_color = modify_rgb(old_color, 1.1, 1.2, 0.9)
            newline = replace_rgba(text, new_color)
    except:
        newline = text
    return newline

new = ""
for line in content:
    new += modify_line(line)

with open(write_filename, "w") as file2:
    file2.write(new)