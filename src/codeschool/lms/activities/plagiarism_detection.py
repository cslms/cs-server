import json


def find_identical_responses(activity, context, key=None, cmp=None, thresh=1):
    """
    Finds all responses with identical response_data in the set of best
    responses for an activity.

    Args:
        activity:
            An activity instance.
        key:
            The result of key(response_data) is used for normalizing the
            different responses in the response set.
        cmp:
            A comparison function that take the outputs of key(x) for a
            pair of responses and return True if the two arguments are to
            be considered equal.
        thresh:
            Minimum threshold for the result of cmp(x, y) to be considered
            plagiarism.
    """

    key = key or (lambda x: x)
    responses = activity.best_submissions(context).values()
    response_data = [(x, key(x.response_data))
                     for x in responses if x is not None]

    # We iterate this list in O^2 complexity by comparing every pair of
    # responses and checking if cmp(data1, data2) returns a value greater
    # than or equal thresh.
    bad_pairs = {}
    cmp = cmp or (lambda x, y: x == y)
    for i, (resp_a, key_a) in enumerate(response_data):
        for j in range(i + 1, len(response_data)):
            resp_b, key_b = response_data[j]
            value = cmp(key_a, key_b)
            if value >= thresh:
                bad_pairs[resp_a, resp_b] = value
    return bad_pairs


def group_identical_responses(activity, context, key=None, keep_single=True):
    key = key or (lambda x: json.dumps(x))
    bad_values = {}
    for response in activity.best_submissions(context).values():
        if response is None:
            continue
        key_data = key(response.response_data)
        response_list = bad_values.setdefault(key_data, [])
        response_list.append(response)

    return bad_values
