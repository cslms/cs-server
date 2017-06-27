module Codeschool.Styles
    exposing
        ( css
        )

{-| CSS style sheets


# Styles

@docs CssClasses, CssIds, css

-}

import Css exposing (..)
import Css.Elements exposing (..)
import Css.Namespace exposing (namespace)


{-| Classes defined in Codeschool -}
type CssClasses
    = HeaderFabIcon


{-| Ids for specific page elements -}
type CssIds
    = Foo


css =
    (stylesheet << namespace "codeschool")
    [class HeaderFabIcon
        [ borderRadius: "50%"
        ]
    ]