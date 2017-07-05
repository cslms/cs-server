module Page.Social exposing (view)

import Codeschool.Model exposing (Model)
import Html exposing (..)
import Html.Attributes exposing (..)
import Ui.Generic exposing (container)
import Ui.Parts exposing (promoSimple, promoTable, simpleHero)


view : Model -> Html msg
view m =
    div []
        [ simpleHero "Social" ""
        , container []
            [ promoTable
                ( promoSimple "record_voice_over"
                    "Blog"
                    []
                    [ text
                        """
                        Create a personal blog that you can share projects and
                        works with your friends and teachers. 
                        """
                    , a [ href "/classrooms/" ] [ text "here" ]
                    ]
                , promoSimple "group"
                    "Friends"
                    []
                    [ text
                        """
                        Manage your friends and add new friends to the list.
                        """
                    ]
                , promoSimple "question_answer"
                    "Forum"
                    []
                    [ text
                        """
                        Engage in discussions.
                        """
                    ]
                )
            ]
        ]
