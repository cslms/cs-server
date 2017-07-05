module Page.Submission exposing (view)

import Codeschool.Model exposing (Model)
import Html exposing (..)
import Html.Attributes exposing (..)
import Ui.Generic exposing (container, icon)
import Ui.Parts exposing (promoSimple, promoTable, simpleHero)


type alias Submission =
    { question : String, points : Int, ok : Bool }


submissions =
    [ Submission "Fibonacci" 100 True
    , Submission "Fibonacci" 0 False
    , Submission "Hello Person" 20 True
    , Submission "Hello" 10 True
    ]


view : Model -> Html msg
view m =
    div []
        [ simpleHero "List of submissions" "Check your last submissions."
        , container []
            [ table []
                [ thead []
                    [ tr []
                        [ th [] [ text "Name" ]
                        , th [] [ text "Points" ]
                        , th [] [ text "Correct" ]
                        ]
                    ]
                , tbody [] (List.map viewSubmission submissions)
                ]
            ]
        ]


viewSubmission : Submission -> Html msg
viewSubmission submission =
    let
        icon_ =
            case submission.ok of
                True ->
                    icon [] "check"

                False ->
                    text "-"
    in
    tr []
        [ td [] [ text submission.question ]
        , td [] [ text (toString submission.points) ]
        , td [] [ icon_ ]
        ]
