"""
Codeschool configuration options
"""

#: If true, forces usernames being equal to the school id for each student.
CODESCHOOL_USERNAME_IS_SCHOOL_ID = False

#: A regular expression for validating school id values. Set it to None to
#: disable validation.
CODESCHOOL_SCHOOL_ID_VALIDATION = None

#: A regular expression describing valid user names.
CODESCHOOL_USERNAME_VALIDATION = None

#: Enable/disable sandboxing. You should always enable sandboxing in production.
CODESCHOOL_SANDBOX = True

#: Enable debug views at _admin/ and _debug/
CODESCHOOL_DEBUG_VIEWS = True

#: Enable a global "Questions" page
CODESCHOOL_GLOBAL_QUESTIONS = True


#: Enable REST api
CODESCHOOL_REST_API = True