module Codeschool.Wagtail
    exposing
        ( StreamField
        , StreamItem
        , render
        )

{-| Support for Watgail types


# Types

@docs StreamItem, StreamField

-}

import Html exposing (..)
import Html.Attributes exposing (..)
import Markdown


{-| A node in a Stream field and its corresponding contents
-}
type StreamItem
    = Markdown String
    | Html String
    | Ignored


{-| A Stream field is simply a list of StreamItem's
-}
type alias StreamField =
    List StreamItem


{-| Render list of description items
-}
render : StreamField -> Html msg
render data =
    let
        description : StreamItem -> Html msg
        description item =
            case item of
                Markdown md ->
                    Markdown.toHtml [ class "cs-markdown" ] md

                Html x ->
                    div [] [ text x ]

                Ignored ->
                    span [] []
    in
    div []
        [ h2 [ class "cs-banner" ]
            [ text "Description" ]
        , article [ class "question-stem" ] <|
            List.map description data
        ]
