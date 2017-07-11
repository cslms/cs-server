module Ui.Layout exposing (page)

import Codeschool.Model exposing (..)
import Codeschool.Msg as Msg exposing (..)
import Html exposing (..)
import Html.Attributes exposing (..)
import Html.Events exposing (..)
import Ui.Footer
import Ui.Generic exposing (..)
import Ui.Header
import Ui.Sidebar exposing (sidebar)


{-| Main page layout
-}
page : Html Msg -> Model -> Html Msg
page content model =
    let
        contentStyle =
            style
                [ ( "min-height", "100vh" )
                , ( "display", "flex" )
                , ( "flex-direction", "column" )
                , ( "justify-content", "space-between" )
                , ( "margin-left", "40px" )
                , ( "padding", "0" )
                ]

        head_ =
            div [ shadow 2 ]
                [ header [] [ Ui.Header.header model ]
                ]

        content_ =
            main_
                [ style
                    [ ( "height", "100%" )
                    , ( "width", "100%" )
                    , ( "padding", "0" )
                    , ( "margin", "0" )
                    , ( "margin-bottom", "auto" )
                    , ( "vertical-align", "top" )
                    , ( "z-index", "0" )
                    ]
                , class "page-content"
                ]
                [ content ]

        foot_ =
            div [ shadow 2 ]
                [ footer [] [ Ui.Footer.footer model ]
                ]

        map a =
            a
    in
    div []
        [ map <| div [] [ sidebar model ]
        , div [ class "content", contentStyle ]
            [ map head_
            , content_
            , map foot_
            ]
        ]


fire : Route -> Html.Attribute Msg
fire route =
    onClick (ChangeRoute route)
