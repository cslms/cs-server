from collections import Mapping
from functools import singledispatch

from bricks.components import BaseComponent
from bricks.components.html5_tags import br
from bricks.helpers import join_classes


def with_class(obj, *classes):
    """
    Add classes to first argument.

    If called with a dictionary, add given classes to a dictionary of keyword
    values and return the  resulting kwargs dictionary.

    If called with a function, decorate the function that returns a tag and add
    the given class to the begin class list.

    Examples:

        >>> kwargs = {'class_': 'foo'}
        >>> with_class(kwargs, 'bar'); kwargs
        {'class_': ['bar', 'foo']}

        >>> @with_class('bar')
        ... def my_div(**kwargs):
        ...     return div(**kwargs)
        >>> str(my_div('data', class_='foo'))
        <div class="foo bar">data</div>
    """

    if isinstance(obj, BaseComponent):
        obj.classes = join_classes(classes, obj.classes)
        return obj

    elif isinstance(obj, Mapping):
        class_ = obj.get('class_')
        obj['class_'] = join_classes(classes, class_)
        return obj

    elif obj is None:
        return None

    elif callable(obj):
        def decorated(*args, **kwargs):
            result = obj(*args, **kwargs)
            return with_class(result, *classes)

        return decorated

    else:
        def decorator(func):
            return with_class(func, *classes)

        return decorator


def tag_join(seq, tag=None):
    """
    Join a list of tags using another tag as a separator.

    Args:
        seq:
            A sequence of tags.
        tag:
            The tag used as separator.

    Returns:
        A sequence of tags.
    """

    tag = tag or br()
    result = []
    for x in seq:
        result.append(x)
        result.append(tag)
    result.pop()
    return result


@singledispatch
def title(obj):
    """
    Return a title string for object.
    """

    try:
        return obj.title
    except AttributeError:
        return str(obj)
