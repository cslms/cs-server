module Ui.Header exposing (..)

{-| The Header component
-}

import Codeschool.Model exposing (..)
import Codeschool.Msg as Msg exposing (..)
import Html exposing (..)
import Html.Attributes exposing (..)
import Html.Events exposing (..)
import Polymer.Paper as Paper exposing (..)
import Ui.Generic exposing (icon, zindex)


{-| View header component.
-}
header : Model -> Html Msg
header model =
    let
        link route txt =
            Paper.button
                [ onClick (ChangeRoute route)
                , slot "top"
                , class "page-header__link"
                ]
                [ div [] [ text txt ] ]

        slot =
            attribute "slot"

        button =
            fab [ class "page-header__user-menu" ] [ icon [] "person" ]

        userMenu =
            menuButton
                [ class "page-header__user-menu"
                , attribute "horizontal-align" "right"
                , attribute "horizontal-offset" "-0"
                , attribute "vertical-offset" "80"
                ]
                [ fab
                    [ slot "dropdown-trigger"
                    , class "page-header__user-menu-button"
                    , attribute "mini" "mini"
                    , attribute "icon" "person"
                    ]
                    []
                , listbox [ slot "dropdown-content", class "page-header__user-menu-content" ]
                    [ div [ class "page-header__user-menu-icon" ] [ icon [] "person" ]
                    , div [ class "page-header__user-menu-title" ] [ h1 [] [ text "Actions" ] ]
                    , item [ onClick (ChangeRoute (Profile model.user.id)) ] [ text "Profile" ]
                    , item [ href "/logout/" ] [ text "Logout" ]
                    ]
                ]

        header =
            div
                [ class "page-header"
                , zindex 10
                ]
                [ span [ class "page-logo title", slot "top" ]
                    [ img
                        [ src "https://codeschool.lappis.rocks/static/img/logo.svg"
                        , onClick (ChangeRoute Index)
                        ]
                        []
                    ]
                , link ClassroomList "Classrooms"
                , link QuestionList "Questions"
                , link Social "Social"
                , icon [ class "page-header__notification" ] "notifications"
                , userMenu
                ]
    in
    div [] [ header ]
