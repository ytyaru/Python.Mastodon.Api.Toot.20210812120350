#!/usr/bin/env python3
# coding: utf8
import requests
import os, sys, argparse, json
def exept_null(f):
    def _wrapper(*args, **kwargs):
        try: return f(*args, **kwargs)
        except: return None
    return _wrapper
class Path:
    @classmethod
    def current(cls, path): # カレントディレクトリからの絶対パス
        return cls.__expand(os.path.join(os.getcwd(), path))
    @classmethod
    def here(cls, path): # このファイルからの絶対パス
        return cls.__expand(os.path.join(os.path.dirname(os.path.abspath(__file__)), path))
    @classmethod
    def __expand(cls, path): # homeを表すチルダや環境変数を展開する
        return os.path.expandvars(os.path.expanduser(path))
class FileReader:
    @classmethod
    @exept_null
    def text(self, path):
        with open(path, mode='r', encoding='utf-8') as f: return f.read().rstrip('\n')
    @classmethod
    def json(self, path):
        with open(path, mode='r', encoding='utf-8') as f: return json.load(f)
class FileWriter:
    @classmethod
    def text(self, path, content):
        with open(path, mode='w', encoding='utf-8') as f: f.write(content)
    @classmethod
    def json(self, path, content):
        with open(path, mode='w', encoding='utf-8') as f: json.dump(content, f)
class Toot:
    def __init__(self):
        self.__base_url = 'https://'
    def __get_base_url(self):
        host = FileReader.text(Path.here('host.txt'))
        return f"https://{host}"
    @property
    def BaseUrl(self, domain=None):
        candidates = [domain, FileReader.text(Path.here('host.txt')), 'mstdn.jp']
        hosts = [c for c in candidates if c is not None]
        return f'https://{hosts[0]}/'
    def toot(self, text):
        #requests.post()
        return self.BaseUrl

if __name__ == "__main__":
    toot = Toot()
    content = '''PythonでAPI を叩いてみた。
#mastodon #api'''
    print(toot.toot(content))

