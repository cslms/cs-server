from codeschool.cli import api
from codeschool.cli.utils import JSONEncodedError, get_parent_from_hint, \
    validate_user, check_write_permissions, normalize_resource_type, get_loader, \
    wrap_json_rpc, resource_to_url


#
# Non-decorated test-friendly methods.
#
def push_resource_worker(data, resource_type, parent, auth):
    """
    Put or update resource to Codeschool.

    Args:
        data:
            Resource contents. Must be a string of data. Binary contents should
            be Base64 encoded.
        resource_type:
            Resource type.
        parent:
            A hint to the parent page for the resource.
        auth:
            Authentication credentials (username, password).

    Returns:
        A JSON encoded message.
    """

    user = validate_user(*auth)
    parent = get_parent_from_hint(parent)
    check_write_permissions(user, parent)
    resource_type = normalize_resource_type(resource_type)

    # Load
    loader = get_loader(resource_type)
    try:
        result = loader(data, parent)
        result.owner = user
        return result
    except (SyntaxError, ValueError) as ex:
        raise JSONEncodedError({
            'error': 'resource',
            'type': str(resource_type),
            'message': str(ex)
        })


def echo_worker(*args, **kwargs):
    """
    Returns an echo. Checks if the CLI API is alive.
    """
    if args and kwargs:
        kwargs['*args'] = args
        return kwargs
    else:
        return args if args else kwargs


#
# Final JSON-RPC end points
#
push_resource = api.dispatcher.add_method(
    wrap_json_rpc(resource_to_url(push_resource_worker)),
    name='push')
echo = api.dispatcher.add_method(echo_worker, name='echo')
