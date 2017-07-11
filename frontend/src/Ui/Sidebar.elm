module Ui.Sidebar exposing (sidebar)

import Codeschool.Model exposing (Model, Route(..))
import Codeschool.Msg as Msg exposing (Msg)
import Html exposing (..)
import Html.Attributes exposing (..)
import Html.Events exposing (..)
import Ui.Generic exposing (..)


{-| The main sidebar component
-}
sidebar : Model -> Html Msg
sidebar model =
    let
        menuitem route icon_ text_ =
            div [ class "sidebar__item" ]
                [ a [ onClick (Msg.ChangeRoute route) ]
                    [ icon [ class "sidebar__icon" ] icon_
                    , span [ class "sidebar__text" ] [ text text_ ]
                    ]
                ]
    in
    div
        [ class "sidebar", zindex 20 ]
        [ menuitem SubmissionList "history" "Last submissions"
        , menuitem ScoreBoard "stars" "Score board"
        , menuitem Progress "timeline" "Progress"
        , menuitem Learn "school" "Learn"
        , menuitem Help "help_outline" "Help"
        ]
