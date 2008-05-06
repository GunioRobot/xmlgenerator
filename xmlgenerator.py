#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright (c) 2005, Nuno Mariz <http://mariz.org>
All rights reserved.

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

    1. Redistributions of source code must retain the above copyright notice, 
       this list of conditions and the following disclaimer.
    
    2. Redistributions in binary form must reproduce the above copyright 
       notice, this list of conditions and the following disclaimer in the
       documentation and/or other materials provided with the distribution.

    3. Neither the name of Django nor the names of its contributors may be used
       to endorse or promote products derived from this software without
       specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

-------------------------------------------------------------------------------

Unicode XML Generator

Usage:

>>> from xmlgenerator import Xml, Node

>>> # Node creation
>>> root = Node('root')
>>> records = Node('blog', 'http://mariz.org', author='Nuno Mariz', title='Nuno Mariz Weblog')

>>> # Append node
>>> root.append(records)
>>> root
<Node: "root">
    
>>> root.render()
u'<root><blog author="Nuno Mariz" title="Nuno Mariz Weblog">http://mariz.org</blog></root>'

>>> xml = Xml(root)
>>> xml.xml
u'<?xml version="1.0" encoding="utf-8"?>\n
<root><blog author="Nuno Mariz" title="Nuno Mariz Weblog">http://mariz.org</blog></root>'

>>> import cStringIO
>>> stream = cStringIO.StringIO()
>>> xml = Xml(root, stream)
>>> print repr(stream.getvalue())
'<?xml version="1.0" encoding="utf-8"?>\n
<root><blog author="Nuno Mariz" title="Nuno Mariz Weblog">http://mariz.org</blog></root>'

"""
    
from xml.sax.saxutils import escape
from types import NoneType
from decimal import Decimal
from datetime import datetime, date, time

ENCODING = 'utf-8'

class Xml(object):
    """
    XML Generator class
    """

    def __init__(self, node, writer=None):
        self.writer = writer
        self.xml = u'<?xml version="1.0" encoding="%s"?>\n%s' % (ENCODING, node.render())
        if self.writer:
            self.writer.write(self.xml)

class Node(object):
    """
    Node Element
    """

    def __init__(self, name, content=None, **kwargs):
        self.name = name
        self.content = self.escape(content)
        self.attributes = dict()
        for name, value in kwargs.items():
            self.attributes[name] = value
        self.nodes = []
        print kwargs

    def __repr__(self):
        return '<Node: "%s">' % self.name

    def __unicode__(self):
        attributes = u''.join([' %s="%s"' % (key, self.escape(value)) for key, value in self.attributes.items()])
        content = None
        if self.content:
            content = self.content
        elif self.nodes:
            content = u''.join([unicode(node) for node in self.nodes])
        if content:
            return u'<%s%s>%s</%s>' % (self.name, attributes, content, self.name)
        return u'<%s%s />' % (self.name, attributes)

    def append(self, node):
        assert isinstance(node, Node), '"node" is not a Node instance'
        self.nodes.append(node)

    def render(self):
        return self.__unicode__()

    def escape(self, value):
        if isinstance(value, bool):
            if value:
                return u'1'
            return u'0'
        if isinstance(value, (NoneType, bool, int, long, datetime, date, time, float, Decimal)):
            return value
        value = escape(value)
        if isinstance(value, basestring):
            if not isinstance(value, unicode):
                value = unicode(value, ENCODING)
        return value
