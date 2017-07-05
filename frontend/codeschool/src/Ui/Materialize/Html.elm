module Ui.Materialize.Html exposing (..)

{-| Helper functions exposing Materialize.css components.

This module reduces boilerplate when using Materialize.css in Elm code.

-}

import Html exposing (..)
import Html.Attributes exposing (..)
import Materialize.Attributes exposing (..)


type alias Attr msg =
    Html.Attribute msg


type alias Attrs msg =
    List (Attr msg)


type alias Children msg =
    List (Html msg)


type alias Elem msg =
    Attrs msg -> Children msg -> Html msg



---- GRIDS AND FLEXBOXES ----


flexrow : Elem msg
flexrow attrs =
    div <| class "row" :: attrs



---- BADGES ----


{-| A simple badge
-}
badge : String -> String -> Html msg
badge caption value =
    span [ attribute "data-badge-caption" caption, class "badge new" ] [ text value ]


{-| A simple badge with flat style
-}
badgeFlat : String -> String -> Html msg
badgeFlat caption value =
    span [ attribute "data-badge-caption" caption, class "badge" ] [ text value ]



---- BUTTONS ----


{-| A button-like anchor
-}
btn : Elem msg
btn attrs =
    a <| class "waves-effect btn" :: attrs

{-| Floating action button
-}
fab : Elem msg
fab attrs =
    a <| class "waves-effect btn btn-floating" :: attrs


{-| A material submit button
-}
submit : Elem msg
submit attrs =
    button <| class "waves-effect waves-light btn" :: type_ "submit" :: attrs



---- LINKS ----


breadcrumbs : List ( Attr msg, String ) -> Html msg
breadcrumbs lst =
    div [ class "nav-wrapper" ]
        (lst |> List.map (\( attr, name ) -> a [ attr ] [ text name ]))



---- ICONS ----


{-| A material icon with attributes
-}
icon : Attrs msg -> String -> Html msg
icon attrs icon =
    i (class "material-icons" :: attrs) [ text icon ]



---- PRELOADERS ----


spinner : Attrs msg -> Html msg
spinner attrs =
    div (class "preloader-wrapper active" :: attrs)
        [ div [ class "spinner-layer spinner-blue" ]
            [ div [ class "circle-clipper left" ]
                [ div [ class "circle" ]
                    []
                ]
            , div [ class "gap-patch" ]
                [ div [ class "circle" ]
                    []
                ]
            , div [ class "circle-clipper right" ]
                [ div [ class "circle" ]
                    []
                ]
            ]
        ]
