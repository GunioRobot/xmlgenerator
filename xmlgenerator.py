#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
A simple unicode XML Generator

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
>>> xml.render()
u'<?xml version="1.0" encoding="utf-8"?>\n
<root><blog author="Nuno Mariz" title="Nuno Mariz Weblog">http://mariz.org</blog></root>'

>>> import cStringIO
>>> stream = cStringIO.StringIO()
>>> xml = Xml(root)
>>> xml.render(stream)
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

    def __init__(self, node):
        self.node = node

    def render(self, writer=None):
        if writer:
            writer.write(u'<?xml version="1.0" encoding="%s"?>\n%s' % (ENCODING, self.node.render()))
        else:
            return u'<?xml version="1.0" encoding="%s"?>\n%s' % (ENCODING, self.node.render())

class Node(object):
    """
    Node Element
    """

    def __init__(self, n, c=None, **kwargs):
        self.name = n
        self.contents = self.escape(c)
        self.attributes = kwargs
        self.nodes = []

    def __repr__(self):
        return '<Node: "%s">' % self.name

    def __unicode__(self):
        attributes = u''.join([' %s="%s"' % (key, self.escape(value)) for key, value in self.attributes.items()])
        content = None
        if self.contents:
            content = self.contents
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
        if isinstance(value, (NoneType, bool, int, long, datetime, date, time, float, Decimal)):
            return value
        value = escape(value)
        if isinstance(value, basestring):
            if not isinstance(value, unicode):
                value = unicode(value, ENCODING)
        return value
