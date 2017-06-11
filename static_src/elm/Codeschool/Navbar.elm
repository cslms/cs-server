module Codeschool.Navbar
    exposing
        ( NavbarMsg(..)
        , render
        )

{-| Navigation bar


# Messages

@docs NavbarMsg


# Rendering functions

@docs render

-}

import Html exposing (..)
import Html.Attributes exposing (..)
import Html.Events exposing (..)


{-| Navbar messages
-}
type NavbarMsg
    = HideToolbar
    | ShowToolbar 


{-| Renders navigation bar
-}
render : Bool -> Html msg
render visible =
    let
        icon =
            i
                [ class "material-icons"
                , style [ ( "position", "absolute" ), ( "right", "20px" ) ]
                ]
                [ text "menu" ]

        content =
            [ div []
                [ nav [ class "cs-nav__block" ]
                    [ p [ class "cs-nav__block-title" ]
                        [ text "Configurações" ]
                    , ul [ class "cs-nav__block-items" ]
                        [ li []
                            [ a [ href "/admin/pages/10/edit/" ]
                                [ text "Edit" ]
                            ]
                        ]
                    ]
                , nav [ class "cs-nav__block" ]
                    [ a [ class "cs-nav__block-title", href "/questions/basic/the-answer/" ]
                        [ text "The Answer" ]
                    , ul [ class "cs-nav__block-items" ]
                        [ li []
                            [ a [ href "/questions/basic/the-answer/submissions/" ]
                                [ text "Submissions" ]
                            ]
                        ]
                    ]
                ]
            , img [ class "cs-nav__dingbat", src "/static/img/dingbat.svg" ]
                []
            ]
    in
    div [ class "cs-nav cs-stripes-layout__sidebar" ] <|
        if visible then
            [ icon ] ++ content
        else
            [ icon ]
