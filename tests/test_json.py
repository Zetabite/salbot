import unittest
import json
import re
from pathlib import Path

json_paths = {
    "faq": Path("./data/faq.json").resolve(),
    "dgl":  Path("./data/dgl.json").resolve(),
    "tos": Path("./data/tos.json").resolve(),
    "badwords":  Path("./data/badwords.json").resolve(),
}

class TestLoadJson(unittest.TestCase):
    def test_load(self):
        for i in json_paths.values():
            with self.subTest(i=i):
                with i.open() as f:
                    res = json.load(f)

class TestFaqJson(unittest.TestCase):
    def setUp(self):
        self.path = json_paths["faq"]
        with self.path.open() as f:
            self.faq = json.load(f)
    
    def test_types(self):
        self.assertIsInstance(self.faq, list)
        for faq in self.faq:
            with self.subTest(faq=faq):
                
                self.assertIsInstance(faq, dict)
                self.assertIsInstance(faq["names"], list)
                self.assertIsInstance(faq["regexs"], list)
                self.assertIsInstance(faq["channels"], str)
                self.assertIsInstance(faq["content"], str)
                
                for name in faq["names"]:
                    with self.subTest(name=name):
                        self.assertIsInstance(name, str)
                
                for regex in faq["regexs"]:
                    with self.subTest(regex=regex):
                        self.assertIsInstance(regex, str)
    
    def test_regex_compile(self):
        for faq in self.faq:
            with self.subTest(faq=faq):
                for regex in faq["regexs"]:
                    with self.subTest(regex=regex):
                        re.compile(regex)

class TestTosbotJson(unittest.TestCase):
    def setUp(self):
        self.tos_path = json_paths["tos"]
        with self.tos_path.open() as f:
            self.tos = json.load(f)
    
        self.dgl_path = json_paths["dgl"]
        with self.dgl_path.open() as f:
            self.dgl = json.load(f)
    
    def test_types(self):
        for json in [self.dgl, self.tos]:
            unique = []
            self.assertIsInstance(json, list)
            for tos in json:
                with self.subTest(tos_dgl=tos):
                    
                    self.assertIsInstance(tos, dict)
                    self.assertIsInstance(tos["names"], list)
                    self.assertIsInstance(tos["info"], str)
                    self.assertIsInstance(tos["content"], str)
                    
                    for name in tos["names"]:
                        with self.subTest(name=name):
                            self.assertIsInstance(name, str)
                            self.assertNotIn(name, unique)
                            unique.append(name)