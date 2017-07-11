module Page.Progress exposing (view)

import Codeschool.Model exposing (Model)
import Html exposing (..)
import Html.Attributes exposing (..)
import Ui.Generic exposing (container)
import Ui.Parts exposing (promoSimple, promoTable, simpleHero)


view : Model -> Html msg
view m =
    div []
        [ simpleHero "Progress" "Statistics and hints about your progress in the platform."
        , container []
            [ promoTable
                ( promoSimple "schedule"
                    "Works and assigments"
                    []
                    [ text
                        """
                        Check the assigments you haven't delivered yet.
                        """
                    , a [ href "/classrooms/" ] [ text "here" ]
                    ]
                , promoSimple "insert_chart"
                    "Statistics"
                    []
                    [ text
                        """
                        Track your performance in all codeschool questions and exercises.
                        """
                    ]
                , promoSimple "live_help"
                    "Hints"
                    []
                    [ text
                        """
                        Let codeschool help you with what exercises you should work on. 
                        """
                    ]
                )
            ]
        ]
