from codeschool.core import get_programming_language

class DataAccess:
    """
    This class is responsible for acessing data from a coding io question submitted
    """

    def get_placeholder(self, language=None):
        """
        Return the placeholder text for the given language.
        """

        key = self.answers.get(language or self.language, None)
        if key is None:
            return self.default_placeholder
        return key.placeholder

    def get_reference_source(self, language=None):
        """
        Return the reference source code for the given language or None, if no
        reference is found.
        """

        if language is None:
            language = self.language
        qs = self.answers.all().filter(
            language=get_programming_language(language))
        if qs:
            return qs.get().source
        return ''

    def filter_user_submission_payload(self, request, payload):
        return dict(language=payload['language'], source=payload['source'])
