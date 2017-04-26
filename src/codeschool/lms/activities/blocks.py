from codeschool import blocks


RESOURCE_BLOCKS = [
    ('paragraph', blocks.RichTextBlock()),
    ('image', blocks.ImageChooserBlock()),
    ('embed', blocks.EmbedBlock()),
    # ('markdown', blocks.MarkdownBlock()),
    ('url', blocks.URLBlock()),
    ('text', blocks.TextBlock()),
    ('char', blocks.CharBlock()),
    # ('ace', blocks.AceBlock()),
    ('bool', blocks.BooleanBlock()),
    ('doc', blocks.DocumentChooserBlock()),
    # ('snippet', blocks.SnippetChooserBlock(GradingMethod)),
    ('date', blocks.DateBlock()),
    ('time', blocks.TimeBlock()),
    ('stream', blocks.StreamBlock([
        ('page', blocks.PageChooserBlock()),
        ('html', blocks.RawHTMLBlock())
    ])),
]
