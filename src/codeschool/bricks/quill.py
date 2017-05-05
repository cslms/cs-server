"""
A brick for the Quill text editor (https://quilljs.com/)
"""

from bricks.helpers import safe
from bricks.html5 import script


def quill_script(id=None, read_only=False, theme='snow'):
    names = dict(
        id=id,
        read_only=str(read_only).lower(),
        theme='snow',
    )

    return \
        script(safe("""
$(function(){
    var editor = new Quill(#%(id)s{
          debug: 'info',
          modules: {
            toolbar: '#%(id)s-toolbar'
          },
          readOnly: %(read_only)s,
          theme: %(theme)r
    });
})
""" % names))
