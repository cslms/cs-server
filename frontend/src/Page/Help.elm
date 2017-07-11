module Page.Help exposing (view)

import Codeschool.Model exposing (Model)
import Html exposing (..)
import Ui.Generic exposing (container)
import Ui.Parts exposing (promoSimple, promoTable, simpleHero)


view : Model -> Html msg
view m =
    div []
        [ simpleHero "Help" ""
        , container []
            [ promoTable
                ( promoSimple "school"
                    "I am a teacher"
                    []
                    [ text
                        """
                        If you are a teacher and want to create a classroom,
                        please contact the site administrator.
                        """
                    ]
                , promoSimple "bug_report"
                    "I found an error!"
                    []
                    [ text
                        """
                        If you think your error is a bug in Codeschool, please
                        submit a bug report in our issue tracker. If you think
                        the problem is with a specific question, discuss it with
                        your teacher.
                        """
                    ]
                , promoSimple "code"
                    "How do I contribute?"
                    []
                    [ text
                        """
                        You can contribute with code, translations, documentation
                        tests, and general discussion in the Project's github
                        at https://github.com/cslms/cs-server/
                        """
                    ]
                )
            ]
        ]
