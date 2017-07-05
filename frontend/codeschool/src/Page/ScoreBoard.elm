module Page.ScoreBoard exposing (view)

import Codeschool.Model exposing (Model)
import Html exposing (..)
import Html.Attributes exposing (..)
import Ui.Generic exposing (container)
import Ui.Parts exposing (promoSimple, promoTable, simpleHero)


type alias Score =
    { name : String, points : Int, position : Int }


scores =
    [ Score "John" 1200 1
    , Score "Paul" 1100 2
    , Score "George" 900 3
    , Score "Ringo" 720 4
    ]


view : Model -> Html msg
view m =
    div []
        [ simpleHero "Top scores" "You are #10, with 42 points."
        , container []
            [ table []
                [ thead []
                    [ tr []
                        [ th [] [ text "Position" ]
                        , th [] [ text "Name" ]
                        , th [] [ text "Points" ]
                        ]
                    ]
                , tbody [] (List.map viewScore scores)
                ]
            ]
        ]


viewScore : Score -> Html msg
viewScore score =
    tr []
        [ td [] [ text (toString score.position) ]
        , td [] [ text score.name ]
        , td [] [ text (toString score.points) ]
        ]
