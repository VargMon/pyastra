############################################################################
# $Id$
#
# Description: Main module of pyastra. Pyastra project.
# Author: Alex Ziranov <estyler _at_ users _dot_ sourceforge _dot_ net>
#    
# Copyright (c) 2005 Alex Ziranov.  All rights reserved.
#
############################################################################
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Library General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
#
############################################################################
"Main module of pyastra"
from pyastra import filters

# trg_t and src_t should be one of (for PICs):
# * file
# * py
# * tree
# * tree_op
# * obj_list
# * obj_list_op
# * asm
# * asm_op
# * bin
# suffix "_op" means optimized

# TODO: Test library.

version='pyastra 0.0.5-prerelease'
MESSAGE=0
WARNING=1
ERROR=2

def get_ports():
    ports=[]
    for mod_n in filters.__all__:
        mod=__import__('pyastra.filters.%s' % mod_n, globals(), locals(), '*')
        for port in mod.get_ports():
            if port not in ports:
                ports += [port]

    ports.sort()
    return ports

def get_procs(port):
    procs=[]
    for mod_n in filters.__all__:
        mod=__import__('pyastra.filters.%s' % mod_n, globals(), locals(), '*')
        for proc in mod.get_procs(port):
            if proc not in procs:
                procs += [proc]

    procs.sort()
    return procs

def get_options():
    opts={}
    for mod_n in filters.__all__:
        mod=__import__('pyastra.filters.%s' % mod_n, globals(), locals(), '*')
        if hasattr(mod, 'get_options'):
            opts[mod_n]=mod.get_options()
    return opts

def crt_options():
    opts={}
    for fopt in get_options().values():
        for opt in fopt:
            if opt.arg:
                opts[opt.lkey]=''
            else:
                opts[opt.lkey]=False
    return opts
    

def get_merged_metas(subnodes):
    """Merges metas of all given subnodes
    WARNING: some data may be lost (if any two of subnodes have
    the same meta keys."""
    meta={}
    for node in subnodes:
        merge_metas(meta, node.meta)
    return meta

def merge_metas(meta1, meta2):
    """Copies meta information from meta2 to meta1 if meta1
    doesn't already have some info with such key."""
    for key in meta2.keys():
        if not meta1.has_key(key):
            meta1[key]=meta2[key]

class Converter:
    def __init__(self, src, select, say=None, trg_t=['asm_op'], src_t='py', opts={}):
        self.caller_say=None
        self.errors=0
        self.warnings=0
        self.messages=0
        opts['caller_select']=select
        opts['converter']=self
        if say:
            self.caller_say=say
        opts.setdefault('debug', False)
        self.src=src
        self.trg_t=trg_t
        self.src_t=src_t
        self.opts=opts
    
    def convert(self):
        b=Branch(self.src, self.opts['caller_select'], self.trg_t, self.src_t, self.opts)
            
        if b.status == Branch.BROKEN:
            raise "Can't convert %s to %s." % (self.src_t, self.trg_t)
        else:
            result=b.get_trg()
            if b.status == Branch.PARTIALLY_RESOLVED:
                print "The following targets weren't achieved:"
                for trg in self.trg_t:
                    if trg not in result.keys():
                        print "    %s" % trg
            ret=[]
            for val in result.values():
                ret+=val
            return ret
        
    # TODO: Add module name to all messages
    def say(self, message, level=MESSAGE, line=None):
        global MESSAGE, WARNING, ERROR
        if level==ERROR:
            self.errors += 1
        elif level==WARNING:
            self.warnings += 1
        else:
            self.messages += 1

        if self.caller_say:
            self.caller_say(message, level, line)

class Option:
    """Option class represents an option that may be pushed to a filter.
    It has the following fields:
      descr: description of the option
      lkey:  long key name
      skey:  short key name (is an arbitrary argument)
      arg:   boolean that describes whether the option needs an argument
             or it doesn't (defaults to False)"""
    
    def __init__(self, descr, lkey, skey=None, arg=False):
        self.descr=descr
        self.skey=skey
        self.lkey=lkey
        self.arg=arg

    
    
class Branch:
    BROKEN=0
    ASK_USER=1
    PARTIALLY_RESOLVED=2
    RESOLVED=3
    
    def __init__(self, src, select, trg_t, src_t, opts):
        self.status=None
        self.subnodes={}
        self.select=select
        self.meta={}
        for mod_n in filters.__all__:
            mod=__import__('pyastra.filters.%s' % mod_n, globals(), locals(), '*')
            if mod.converts_from == src_t:
                if opts['debug']:
                    print '%s {' % mod_n
                fltr=mod.Filter(src, opts)
                if opts['debug']:
                    print '  meta:', fltr.meta
                if fltr.modified:
                    if mod.converts_to in trg_t:
                        self.add_subnode(fltr, mod.converts_to)
                            
                        if len(trg_t) > 1:
                            n_trg=filter(lambda x: x != mod.converts_to, trg_t)
                            self.fork(fltr.data, select, n_trg, mod.converts_to, opts)
                    else:
                        self.fork(fltr.data, select, trg_t, mod.converts_to, opts, fltr.meta)
                if opts['debug']:
                    print '}'
                        
        if len(self.subnodes)==0:
            self.status=Branch.BROKEN
        elif self.subnodes.has_key('branches'):
            self.status=Branch.ASK_USER
        else:
            self.status=Branch.RESOLVED
            for trg in trg_t:
                if self.subnodes.has_key(trg):
                    if len(self.subnodes[trg]) > 1:
                        self.status=Branch.ASK_USER
                        break
                else:
                    self.status=Branch.PARTIALLY_RESOLVED
        
        if opts['debug']:
            print ('BROKEN', 'ASK_USER', 'PARTIALLY_RESOLVED', 'RESOLVED')[self.status]

    def fork(self, src, select, trg_t, src_t, opts, meta=None):
        """Forks the current branch and adds its subnodes to current branch's
           subnodes.
           Returns the status of the subbranch."""
        b=Branch(src, select, trg_t, src_t, opts)
        
        if b.status == Branch.ASK_USER:
            self.add_subnode(b, 'branches', meta=meta)
        elif b.status >= Branch.PARTIALLY_RESOLVED:
            self.add_subnode(b.subnodes, meta=meta)
        return b.status

    def add_subnode(self, subnode, trg_t=None, meta=None):
        """Adds a subnode to current branch.
           Supports items, lists, tuples. Also other kinds of subnode-dicts
           merging is supported"""
        global merge_metas

        if isinstance(subnode, dict):
            for key in subnode.keys():
                self.add_subnode(subnode[key], key, meta)
        else:
            t=self.subnodes.setdefault(trg_t, [])
            if isinstance(subnode, list) or isinstance(subnode, tuple):
                if meta:
                    for node in subnode:
                        merge_metas(node.meta, meta)
                t+=subnode
            else:
                if meta:
                    merge_metas(subnode.meta, meta)
                t+=[subnode]

    def get_trg(self):
        global merge_metas
        assert(self.status != Branch.BROKEN)
        
        if self.status == Branch.ASK_USER:
            if self.subnodes.has_key('branches'):
                for b in self.subnodes['branches']:
                    self.add_subnode(b.get_trg())

                del self.subnodes['branches']

            for key in self.subnodes:
                if len(self.subnodes[key]) > 1:
                    self.subnodes[key]=self.select(self.subnodes[key])

        for key in self.subnodes:
            merge_metas(self.meta, self.subnodes[key][0].meta)
                             
        for key in self.subnodes:
            merge_metas(self.subnodes[key][0].meta, self.meta)
            
        return self.subnodes
