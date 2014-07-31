BOLD = "\002"
ITALIC = "\026"
UNDERLINE = "\037"
RESET = "\017"

_all = [ BOLD, ITALIC, UNDERLINE, RESET ]

def remove_colors(string):
    for code in _all:
        string = string.replace(code, '')
    return string
