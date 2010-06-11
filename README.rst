
xmlgenerator.py
===============

xmlgenerator.py is a simple unicode XML Generator made in python.

Usage:
------

>>> from xmlgenerator import Xml, Element


Element creation

>>> root = Element('root')
>>> records = Element('blog', 'http://mariz.org', dict(author='Nuno Mariz', title='Nuno Mariz Weblog'))


Append a child element

>>> root.append(records)
>>> root
<Element: "root">

>>> root.render()
u'<root><blog author="Nuno Mariz" title="Nuno Mariz Weblog">http://mariz.org</blog></root>'


Xml document creation

>>> xml = Xml(root)
>>> xml.render()
u'<?xml version="1.0" encoding="utf-8"?>\n
<root><blog author="Nuno Mariz" title="Nuno Mariz Weblog">http://mariz.org</blog></root>'


Writing contents to a file or a writer

>>> import cStringIO
>>> output = cStringIO.StringIO()
>>> xml = Xml(root)
>>> xml.render(output)
>>> print output.getvalue()
<?xml version="1.0" encoding="utf-8"?>
<root><blog author="Nuno Mariz" title="Nuno Mariz Weblog">http://mariz.org</blog></root>

>>> output.close()

>>> # Writing contents to a file
>>> xml = Xml(root)
>>> xml.write('blogs.xml')


Changing the global Xml encoding

>>> Xml.encoding = 'iso-8859-1' # The default is utf-8
