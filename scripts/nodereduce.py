"""
Reduces the size of the node_modules folder.
"""

import re
import os
import hashlib
from collections import Counter, defaultdict
from pprint import pprint

dirs_blacklist = {
    'tests',
    'docs',
}

files_blacklist = {
    'README.md',
    'package.json',
}

extensions_blacklist = {
    '.test.js',
}

regex_blacklist = [
]


class FileInfo:
    @property
    def used_space(self):
        return 0 if self.is_link else self.size
        
    @property
    def ext(self):
        return os.path.splitext(self.name)[1]

    def __init__(self, name, size=None, hash=None, destination=None, is_link=False):
        self.name = name
        self.size = size
        self.hash= hash
        self.destination = destination
        self.is_link = is_link
        

class DedupJob:
    def __init__(self, destination='node_modules.shadow', source='node_modules'):
        self.hash_owner = {}
        self.hash_counter = Counter()
        self.path_to_hash = {}
        self.path_to_path = {}
        self.file_info = {}
        self.destination = destination
        self.source = source
        self.source_size = 0
        self.dest_size = 0
        
    def add(self, filename):
        if not filename.startswith(self.source):
            raise ValueError('path outside %r: %r' % (self.source, filename))
        
        data, size = self.read(filename)
        self.source_size += size
        hash = self.hash(filename, data)
        self.hash_counter[hash] += 1
        self.path_to_hash[filename] = hash
        destination = self.destination + filename[len(self.source):]
            
        kwargs = {'size': size, 'destination': destination, 'hash': hash}
        self.file_info[filename] = fileinfo = FileInfo(filename, **kwargs) 
        
        try:
            owner = self.hash_owner[hash]
            
        # Original data
        except KeyError:
            self.path_to_path[filename] = destination
            self.hash_owner[hash] = filename
            self.write(filename, destination, data)
        
        # File already appeared before
        else:
            owner_destination = self.path_to_path[owner]
            self.path_to_path[filename] = owner_destination
            self.link(owner_destination, destination, data)
            fileinfo.is_link = True
       
    def _assure_has_dir(self, path):
        dirname = os.path.dirname(path)
        if os.path.exists(dirname):
            return
            
        dirname, *tail = path.split(os.path.sep)
        tail.reverse()
        while tail:
            if not os.path.exists(dirname):
                os.mkdir(dirname)
            dirname = os.path.join(dirname, tail.pop())
        
    def write(self, frompath, topath, data):
        self._assure_has_dir(topath)
        with open(topath, 'wb') as F:
            F.write(data) 
        
    def link(self, frompath, topath, data):
        self._assure_has_dir(topath)
        os.symlink(frompath, topath)
        
    def hash(self, filename, data):
        basename = os.path.basename(filename)
        hasher = hashlib.md5(data)
        return hasher.digest()
        
    def read(self, filename):
        """
        Return a tuple with (data, size) for the given file.
        """
        
        with open(filename, 'rb') as F:
            data = F.read()
        return data, len(data)
        
    def report(self):
        owner = self.hash_owner
        counter = Counter({owner[k]: v for k, v in self.hash_counter.items() if v > 1})
        common = counter.most_common()
        common.reverse()
        print('Most common files')
        pprint(common)
        print('-' * 80) 
        
        ext_sizes = Counter()
        ext_saved = Counter()
        for fileinfo in self.file_info.values():
            ext_sizes[fileinfo.ext] += fileinfo.size
            if fileinfo.is_link:
                ext_saved[fileinfo.ext] += fileinfo.size
        print('\n\nMost used files')
        pprint(ext_sizes.most_common())
        print('-' * 80)
        
        print('\n\nSaved space') 
        pprint(ext_saved.most_common())
        

def accept_file(filename, at_dir=None):
    if filename in files_blacklist:
        return False
    for ext in extensions_blacklist:
        if filename.endswith(ext):
            return False
    for regex in regex_blacklist:
        if regex.match(filename):
            return False
    return True


def accept_dir(dirname):
    basename = os.path.basename(base)
    if basename in dirs_blacklist:
        return False
    return True


dedup = DedupJob('node_modules.shadow')
for base, dirs, files in os.walk('node_modules'):
    if not accept_dir(base):
        continue
         
    for f in files:
        if accept_file(f, base):
            dedup.add(os.path.join(base, f))
            

# print(dedup.hash_count.most_common())
print(dedup.report())

