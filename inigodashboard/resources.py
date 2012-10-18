from fanstatic import Library
from fanstatic import Resource
from fanstatic import Group
#from js.lesscss import LessResource
from js.bootstrap import bootstrap

library = Library('inigodashboard', 'resources')

css_resource = Resource(library, 'main.css', depends=[bootstrap])

js_resource = Resource(library, 'main.js', bottom=True, depends=[css_resource])

tablesorter = Resource(library, 'jquery.tablesorter.js',
                        minified='jquery.tablesorter.min.js',
                        depends=[bootstrap])

#less_resource = LessResource(library, 'main.less')

resources = Group([css_resource, js_resource, tablesorter
#                     less_resource,
                    ])


def pserve():
    """A script aware of static resource"""
    import pyramid.scripts.pserve
    import pyramid_fanstatic
    import os

    dirname = os.path.dirname(__file__)
    dirname = os.path.join(dirname, 'resources')
    pyramid.scripts.pserve.add_file_callback(
                pyramid_fanstatic.file_callback(dirname))
    pyramid.scripts.pserve.main()
