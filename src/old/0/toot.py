#!/usr/bin/env python3
# coding: utf8
import requests
import os, sys, argparse, json, urllib.parse
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
class Authenticator:
    @property
    def Token(self):
        token = FileReader.text(Path.here('token.txt'))
        if token is None: raise Exception('token.txtがありません。マストドンのインスタンスサーバでアカウントを作り、アプリを作って、アクセストークンを取得し、その値をtoken.txtに書いて保存してください。')
        return token
#        return FileReader.text(Path.here('token.txt'))
class Api:
    def __init__(self):
        self.__auth = Authenticator()
    @property
    def Auth(self): return self.__auth
    @property
    def BaseUrl(self, domain=None):
        candidates = [domain, FileReader.text(Path.here('host.txt')), 'mstdn.jp']
        hosts = [c for c in candidates if c is not None]
        return f'https://{hosts[0]}/'
    @property
    def Header(self):
        return {
            'User-Agent': 'Mozilla/5.0 (X11; CrOS armv7l 13597.84.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.187 Safari/537.36',
#            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.Auth.Token}',
        }
        
class Toot(Api):
    @property
    def ApiUrl(self): return urllib.parse.urljoin(self.BaseUrl, 'api/v1/statuses')
    def toot(self, text):
        data = {}
        data['status'] = text
        data['media_ids'] = []
        data['poll'] = {'options':[], 'expires_in':0}
        res = requests.post(self.ApiUrl, headers=self.Header, data=data)
        print(res.status_code)
        print(res.headers)
        print(res.text)
        return res.json()

if __name__ == "__main__":
    toot = Toot()
    content = '''api/v1/statuses で空の引数media_ids,pollを消してみる。403エラー。必須らしい。
#mastodon #api'''
    print(json.dumps(toot.toot(content)))

