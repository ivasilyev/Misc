#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import os
import sys


class Replacer:
    _BOTH_CASE_CHARS = """
        а,a
        е,e
        о,o
        р,p
        с,c
        х,x
        """
    _UPPERCASE_CHARS = """
        З,3
        К,K
        М,M
        Н,H
        Т,T
        """
    _LOWERCASE_CHARS = "у,y"

    def __init__(self):
        self.replacements = []
        for char_list in (self._UPPERCASE_CHARS, self._LOWERCASE_CHARS):
            for pair in self.parse_replacements(char_list):
                self.replacements.append(pair)
        for pair in self.parse_replacements(self._BOTH_CASE_CHARS, convert=True):
            self.replacements.append(pair)

    @staticmethod
    def parse_replacements(s: str, convert: bool = False):
        out = []
        for line in re.split("[\r\n]+", s):
            line = line.strip()
            if len(line) < 3:
                continue
            chars = re.split("[,]+", line)
            if len(chars) > 1:
                out.append(chars)
            if convert:
                out.append(list(map(lambda x: x.upper(), chars)))
        return out

    def replace(self, s: str):
        for replacement_pair in self.replacements:
            s = s.replace(*replacement_pair)
        return s


if __name__ == '__main__':
    target = ""
    try:
        target = sys.argv[1]
    except IndexError:
        raise ValueError("You need to specify file or string!")
    string = target
    if os.path.isfile(target):
        with open(file=target, mode="r", encoding="utf-8") as f:
            string = f.read()
            f.close()
    replacer = Replacer()
    output = replacer.replace(string)
    if not os.path.isfile(target):
        print(output)
    else:
        target1, target2 = os.path.splitext(target)
        with open(file="{}_cyr2lat.{}".format(target1, target2), mode="w", encoding="utf-8") as f:
            f.write(output)
            f.close()
