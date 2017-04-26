def markdown_to_blocks(source):
    """
    Convert a markdown source string to a sequence of blocks.
    """

    # Maybe we'll need a more sophisticated approach that mixes block types
    # and uses headings, markdown blocks and extended markdown syntax. Let us
    # try the simple dumb approach first.
    if isinstance(source, bytes):
        source = source.decode('utf-8')
    block_list = [('markdown', source)]
    return block_list


def blocks_to_markdown(children):
    """
    Convert a sequence of stream children to markdown.
    """

    lines = []
    for child in children:
        if child.block.name == 'markdown':
            lines.append(child.value)
            lines.append('')
        else:
            raise ValueError('cannot convert stream block: %s' %
                             child.block.name)
    return '\n'.join(lines)
