#!/usr/bin/env python3
# coding: utf8
import requests
import os, sys, argparse, json, urllib.parse
from string import Template
from lib import exept_null, Path, FileReader, FileWriter, Authenticator, Api
class Toot(Api):
    @property
    def ApiUrl(self): return urllib.parse.urljoin(self.BaseUrl, 'api/v1/statuses')
    def toot(self, text):
        data = {}
        data['status'] = text
        data['media_ids'] = []
        data['poll'] = {'options':[], 'expires_in':0}
        print(self.Header, file=sys.stderr)
        print(data, file=sys.stderr)
        res = requests.post(self.ApiUrl, headers=self.Header, data=data)
        print(res.status_code, file=sys.stderr)
        print(res.headers, file=sys.stderr)
        print(res.text, file=sys.stderr)
        return res.json()
class App:
    @classmethod
    def Version(self): return '0.0.1'
    @classmethod
    def Help(self):
        t = Template(FileReader.text(Path.here('help.txt')))
        return t.substitute(this=Path.this_name(), version=self.Version())
    @classmethod
    def Toot(self, content): return json.dumps(Toot().toot(content))
class Cli:
    def __cmd(self, text):
        print(text)
        sys.exit(0)
    def __get_content(self):
        if 1 < len(sys.argv): return '\n'.join(sys.argv[1:])
        else: return sys.stdin.read().rstrip('\n')
    def __parse(self):
        if 1 < len(sys.argv):
            if   '-h' == sys.argv[1]: self.__cmd(App.Help())
            elif '-v' == sys.argv[1]: self.__cmd(App.Version())
        self.__cmd(App.Toot(self.__get_content()))
    def run(self): self.__parse()
if __name__ == "__main__":
    Cli().run()
