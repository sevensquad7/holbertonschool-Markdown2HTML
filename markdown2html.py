#!/usr/bin/python3
"""Markdown to HTML"""


import re
import sys
import hashlib


dictwrap = {"#": ["<h1>", "</h1>"],
            "##": ["<h2>", "</h2>"],
            "###": ["<h3>", "</h3>"],
            "####": ["<h4>", "</h4>"],
            "#####": ["<h5>", "</h5>"],
            "######": ["<h6>", "</h6>"],
            "-": ["<li>", "</li>", "<ul>\n", "\n</ul>"],
            "*": ["<li>", "</li>", "<ol>\n", "\n</ol>"]}


def wraptext(text, tag1, tag2):
    """wrap a text with two tags"""
    return tag1 + text + tag2


def markdown2html(mdFilename, HTMLFilename):
    """Convert a .md file into a .html format"""
    with open(mdFilename, "r") as mdFile:
        lines = mdFile.read().split("\n\n")

    htmlLines = []
    for line in lines:
        if line == '':
            continue
        if line == lines[-1]:
            line = line[:-1]

        md5Tags = re.findall("\[\[[^\[\]]*\]\]", line)
        for tag in md5Tags:
            if tag != '':
                aux = tag.replace('[[', '')
                aux = aux.replace(']]', '')
                encrypt = hashlib.md5()
                encrypt.update(aux.encode("utf-8"))
                encrypt = encrypt.hexdigest()
                line = line.replace(tag, encrypt)

        noCTags = re.findall("\(\([^\(\)]*\)\)", line)
        for tag in noCTags:
            if tag != '':
                aux = tag.replace('((', '').replace('))', '')
                aux = aux. replace('c', '').replace('C', '')
                line = line.replace(tag, aux)

        boldTags = re.findall("\*\*[^\*\*]*\*\*", line)
        for tag in boldTags:
            if tag != '':
                line = line.replace(tag, wraptext(tag.split("**")[1],
                                                  "<b>", "</b>"))

        emTags = re.findall("__[^__]*__", line)
        for tag in emTags:
            if tag != '':
                line = line.replace(tag, wraptext(tag.split("__")[1],
                                                  "<em>", "</em>"))

        items = line.split("\n")
        prevItems = items.copy()
        wrapping = False
        for idx, item in enumerate(items):
            initialTag = item.split(" ")[0]
            if initialTag in dictwrap.keys():
                item = item.replace('{} '.format(initialTag), '')
            if item == items[0] or wrapping is False:
                if initialTag not in dictwrap.keys():
                    wrapping = True
                    item = '<p>\n{}'.format(item)
                    if idx == len(items) - 1:
                        item = '{}\n</p>'.format(item)
                elif initialTag in ["-", "*"]:
                    wrapping = True
                    item = '{}{}{}{}'.format(dictwrap[initialTag][2],
                                             dictwrap[initialTag][0], item,
                                             dictwrap[initialTag][1])
                    if idx == len(items) - 1:
                        item = '{}{}'.format(item, dictwrap[initialTag][3])
                else:
                    item = wraptext(item, dictwrap[initialTag][0],
                                    dictwrap[initialTag][1])
            else:
                initialPrevTag = prevItems[idx - 1].split(" ")[0]
                if initialPrevTag != initialTag:
                    if initialPrevTag not in dictwrap.keys()\
                            and initialTag not in dictwrap.keys():
                        items[idx - 1] = '{}\n<br/>'.format(items[idx - 1])
                    elif initialPrevTag not in dictwrap.keys():
                        wrapping = False
                        items[idx - 1] = '{}\n</p>'.format(items[idx - 1])
                    elif initialPrevTag in ["-", "*"]:
                        wrapping = False
                        items[idx - 1] = '{}{}'\
                                         .format(items[idx - 1],
                                                 dictwrap[initialPrevTag][3])
                if initialTag in dictwrap.keys():
                    item = wraptext(item, dictwrap[initialTag][0],
                                    dictwrap[initialTag][1])
                if idx == len(items) - 1:
                    if initialTag not in dictwrap.keys():
                        item = '{}\n</p>'.format(item)
                    elif initialTag in ["-", "*"]:
                        item = '{}{}'.format(item, dictwrap[initialTag][3])
            items[idx] = item
        htmlLines.append("\n".join(items))

    with open(HTMLFilename, "w") as HTMLFile:
        for line in htmlLines:
            line += "\n"
            HTMLFile.write(line)


if __name__ == "__main__":
    """main program"""
    if len(sys.argv) <= 2:
        sys.stderr.write("Usage: ./markdown2html.py README.md README.html\n")
        sys.exit(1)
    try:
        markdown2html(sys.argv[1], sys.argv[2])
    except FileNotFoundError:
        sys.stderr.write("Missing <filename>\n")
        sys.exit(1)
