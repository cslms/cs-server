module Codeschool.Page
    exposing
        ( contentHeader
        , footer
        )

{-| View functions for common Codeschool elements.


# Views

@docs  contentHeader

-}

import Html exposing (..)
import Html.Attributes exposing (..)




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
