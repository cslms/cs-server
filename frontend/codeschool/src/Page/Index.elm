module Page.Index exposing (view)

import Codeschool.Model exposing (Model)
import Html exposing (..)
import Html.Attributes exposing (..)
import Ui.Generic exposing (container)
import Ui.Parts exposing (promoSimple, promoTable, simpleHero)


view : Model -> Html msg
view m =
    div []
        [ simpleHero "Welcome to Codeschool" ""
        , container []
            [ promoTable
                ( promoSimple "assignment"
                    "Enroll"
                    []
                    [ text
                        """
                        Codeschool provides many programming-based courses.
                        If you are not registered, please click
                        """
                    , a [ href "/classrooms/" ] [ text "here" ]
                    ]
                , promoSimple "search"
                    "Discover"
                    []
                    [ text
                        """
                        You can find tutorials, exercises and other learning
                        materials that are not associated with any course.
                        """
                    ]
                , promoSimple "question_answer"
                    "Interact"
                    []
                    [ text
                        """
                        You can invite your friends to be part of your contacts
                        network and collaborate and challenge them.
                        """
                    ]
                )
            ]
        ]
