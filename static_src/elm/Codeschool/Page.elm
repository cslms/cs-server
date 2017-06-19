module Codeschool.Page
    exposing
        ( contentHeader
        , footer
        , header
        )

{-| View functions for common Codeschool elements.


# Views

@docs header, footer,contentHeader

-}

import Html exposing (..)
import Html.Attributes exposing (..)


{-| Exhibit the Codeschool header element on page.
-}
header : Html msg
header =
    div [ class "cs-head mdl-cell mdl-cell--12-col" ]
        [ div [ class "cs-logo" ]
            [ img [ class "cs-logo__img", src "/static/img/logo.svg" ]
                []
            ]
        , nav [ class "cs-head__nav" ]
            [ div [ class "cs-head__links" ]
                [ a [ href "/questions/" ]
                    [ text "Questions" ]
                ]
            , span [ class "cs-head__fab mdl-button mdl-js-button mdl-button--fab mdl-button--colored fab-button", id "cs-head--dropdown-trigger" ]
                [ span [ class "dropdown-trigger" ]
                    [ text "a" ]
                ]
            , ul [ class "mdl-menu mdl-menu--bottom-left mdl-js-menu mdl-js-ripple-effect", for "cs-head--dropdown-trigger" ]
                [ li [ class "mdl-menu__item" ]
                    [ a [ href "/profile/" ]
                        [ text "Profile" ]
                    ]
                , li [ class "mdl-menu__item" ]
                    [ a [ href "/auth/logout/" ]
                        [ text "Logout" ]
                    ]
                ]
            ]
        ]


{-| Display the footer element of a Codeschool page
-}
footer : Html msg
footer =
    div [ class "cs-foot mdl-cell mdl-cell--12-col" ]
        [ div [ class "cs-foot__copyright" ]
            [ p []
                [ text "Copyright 2016 -"
                , a
                    [ href "http://github.com/fabiommendes/codeschool" ]
                    [ text "Codeschool" ]
                ]
            , p []
                [ text "Site gerenciado por Fábio M. Mendes na UnB/Gama." ]
            ]
        ]


{-| Displays the content header title and subtitle.
-}
contentHeader : String -> String -> Html msg
contentHeader title subtitle =
    div []
        [ h1 []
            [ text title ]
        , p []
            [ text
                (if String.isEmpty subtitle then
                    title
                 else
                    subtitle
                )
            ]
        ]
