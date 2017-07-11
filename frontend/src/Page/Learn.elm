module Page.Learn exposing (view)

import Codeschool.Model exposing (Model)
import Html exposing (..)
import Ui.Generic exposing (container)
import Ui.Parts exposing (promoSimple, promoTable, simpleHero)


view : Model -> Html msg
view m =
    div []
        [ simpleHero
            "Learning resources"
            "This page presents all learning resources that are available to any user."
        , container []
            [ promoTable
                ( promoSimple "school"
                    "Tutorials"
                    []
                    [ text
                        """
                        A few programming tutorials. Even if you are in an 
                        advanced course, the content here can be useful if you 
                        are feeling rusty... 
                        """
                    ]
                , promoSimple "code"
                    "Questions"
                    []
                    [ text
                        """
                        A list of questions that you can use to practice and 
                        challenge your friends. Who can write the better code?
                        """
                    ]
                , promoSimple "code"
                    "Documentation"
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
