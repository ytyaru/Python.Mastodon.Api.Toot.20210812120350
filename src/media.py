#!/usr/bin/env python3
# coding: utf8
import requests
import os, sys, argparse, json, urllib.parse
from string import Template
from lib import exept_null, Path, FileReader, FileWriter, Authenticator, Api
from abc import ABCMeta, abstractmethod
import mimetypes

# https://docs.joinmastodon.org/ja/user/posting/#attachments
class Limit(metaclass=ABCMeta):
    @abstractmethod
    def num(self): pass
    @abstractmethod
    def size(self): pass
    @abstractmethod
    def formats(self): pass
class ImageLimit(Limit):
    def num(self): return 4
    def size(self): return 8,000,000
    def formats(self): return ['png', 'gif', 'jpg', 'jpeg']
    def git_animation(self): return 'mp4'
class MovieLimit(Limit):
    def num(self): return 1
    def size(self): return 40,000,000
    def formats(self): return ['mp4', 'm4v', 'mov', 'webm']
    def bit_rate(self): return 1300
    def frame_rate(self): return 60
class AudioLimit(Limit):
    def num(self): return 1
    def size(self): return 40,000,000
    def formats(self): return ['mp3', 'ogg', 'wav', 'flac', 'opus', 'aac', 'm4a', '3gp']
# https://docs.joinmastodon.org/methods/statuses/media/
class Media(Api):
    @property
    def ApiUrl(self): return urllib.parse.urljoin(self.BaseUrl, 'api/v1/media')
    def media(self, path, thumbnail=None, description=None, focus=None):
        files = {}
        files['file'] = self.__file_tuple(path)
        if thumbnail is not None: files['thumbnail'] = self.__file_tuple(thumbnail)
        params = {}
        if description is not None: params['description'] = description
        if focus is not None: params['focus'] = focus
        print(self.Header, file=sys.stderr)
        print(params, file=sys.stderr)
        print(files, file=sys.stderr)
        res = requests.post(self.ApiUrl, headers=self.Header, files=files, params=params)
        print(res.status_code, file=sys.stderr)
        print(res.headers, file=sys.stderr)
        print(res.text, file=sys.stderr)
        return res.json()
    def __file_tuple(self, path):
        return (path, open(path,'rb').read(), mimetypes.guess_type(path)[0])
class App:
    @classmethod
    def Version(self): return '0.0.1'
    @classmethod
    def Help(self):
        t = Template(FileReader.text(Path.here('help/media.txt')))
        return t.substitute(this=Path.this_name(), version=self.Version())
    @classmethod
    def Media(self, *args, **kwargs): return json.dumps(Media().media(*args, **kwargs))
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
