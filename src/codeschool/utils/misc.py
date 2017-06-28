def update_state(obj, state):
    """
    Update state of object using values from a state dictionary.
    """

    for attr, value in state.items():
        setattr(obj, attr, value)
