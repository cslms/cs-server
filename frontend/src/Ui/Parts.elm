module Ui.Parts
    exposing
        ( promoSimple
        , promoTable
        , simpleHero
        )

{-| A module with simple reusable UI bits. All elements are simple functions
that receive simple basic Elm data types.
-}

import Html exposing (..)
import Html.Attributes exposing (..)
import Ui.Generic exposing (container, icon)


--------------------------------------------------------------------------------
-- Hero: a title display that emphasizes the main content of your webpage
--------------------------------------------------------------------------------


{-| A simple hero element with a title and a short description
-}
simpleHero : String -> String -> Html msg
simpleHero title description =
    div
        [ class "simple-hero" ]
        [ container []
            [ h1 [ class "simple-hero__title" ] [ text title ]
            , p [ class "simple-hero__description" ] [ text description ]
            ]
        ]



--------------------------------------------------------------------------------
-- Promo table: display 3 cards with content
--------------------------------------------------------------------------------


{-| Ensure promoTable function only receives Promo objects
-}
type Promo msg
    = Promo (Html msg)


{-| Simple promo table container. Its children should be Promo instances
-}
promoTable : ( Promo msg, Promo msg, Promo msg ) -> Html msg
promoTable ( c1, c2, c3 ) =
    div [ class "promo-table " ]
        [ renderPromo c1
        , renderPromo c2
        , renderPromo c3
        ]


{-| A promo table child with an icon, title and content.
-}
promoSimple : String -> String -> List (Attribute msg) -> List (Html msg) -> Promo msg
promoSimple icon_ title attrs children =
    let
        wrap =
            if List.isEmpty attrs then
                \x -> x
            else
                \x -> a attrs [ x ]

        children_ =
            icon [] icon_
                :: h1 [] [ text title ]
                :: children
    in
    Promo <| div [ class "promo-simple" ] children_


renderPromo : Promo msg -> Html msg
renderPromo promo =
    case promo of
        Promo el ->
            el
