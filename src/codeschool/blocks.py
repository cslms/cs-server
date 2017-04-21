#
# One-stop shop for wagtail blocks
#

# flake8: noqa
from wagtail.wagtailcore.blocks import *
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailsnippets.blocks import SnippetChooserBlock
from wagtail.wagtaildocs.blocks import DocumentChooserBlock
from wagtail.wagtailembeds.blocks import EmbedBlock
from wagtail.contrib.table_block.blocks import TableBlock
from wagtail.wagtailcore.rich_text import RichText
from codeschool.vendor.wagtailmarkdown.blocks import MarkdownBlock
