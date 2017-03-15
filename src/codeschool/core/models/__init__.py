from . import managers
from .fileformat import ProgrammingLanguage, FileFormat, programming_language
from .syspages import RogueRoot, HiddenRoot
from .config_options import ConfigOption, DataEntry
from codeschool.core.config_dict import ConfigDict, DataDict

ConfigDict._model = ConfigOption
DataDict._model = DataEntry