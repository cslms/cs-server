module Codeschool.Utils
    exposing
        ( icon
        , iconAttrs
        )

{-| Utility functions


# View functions

@docs icon, iconAttrs

-}

import Html exposing (..)
import Html.Attributes exposing (..)


{-| Display an Mdl icon
-}
icon : String -> Html msg
icon icon =
    i [ class "material-icons" ] [ text icon ]


{-| A Mdl icon with attributes
-}
iconAttrs : List (Attribute msg) -> String -> Html msg
iconAttrs attrs icon =
    let
        attrs_ =
            class "material-icons" :: attrs
    in
    i attrs_ [ text icon ]
