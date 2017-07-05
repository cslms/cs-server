module Ui.Materialize.Attributes exposing (..)

{-| Helper functions for materialize attributes
-}

import Html
import Html.Attributes exposing (..)
import String exposing (..)


type alias Attr msg =
    Html.Attribute msg


type Waves
    = WavesLight
    | WavesRed
    | WavesYellow
    | WavesOrange
    | WavesPurple
    | WavesGreen
    | WavesTeal



---- EFFECTS ----


waves : Waves -> Attr msg
waves kind =
    class ("waves-" ++ (toString kind |> toLower |> dropRight 5))



---- COLORS ----


{-| Mark element as red
-}
red : Attr msg
red =
    class "red"


{-| Mark element as blue
-}
blue : Attr msg
blue =
    class "blue"


{-| Mark element as teal
-}
teal : Attr msg
teal =
    class "teal"


white : Attr msg
white =
    style [ ( "background-color", "white" ) ]


{-| White text style
-}
whiteText : Attr msg
whiteText =
    class "white-text"



---- STYLES ----


{-| Shadow depth. Must be a number between 0 and 5
-}
shadow : Int -> Attr msg
shadow n =
    let
        m =
            if n < 0 then
                0
            else if n > 5 then
                5
            else
                n
    in
    class <| "z-depth-" ++ toString m


{-| Z-index of element
-}
zindex : Int -> Attr msg
zindex n =
    style [ ( "z-index", toString n ) ]



---- SIZES ----


tiny : Attr msg
tiny =
    class "tiny"


small : Attr msg
small =
    class "small"


medium : Attr msg
medium =
    class "medium"


large : Attr msg
large =
    class "large"



---- GENERIC STATES ----


disabled : Attr msg
disabled =
    class "disabled"



---- COMPONENT STATES ----


btnLarge : Attr msg
btnLarge =
    class "btn-large"


btnFlat : Attr msg
btnFlat =
    class "btn-flat"


btnFloating : Attr msg
btnFloating =
    class "btn-floating"



---- GRIDS AND FLEXBOXES ----


col : Int -> Attr msg
col n =
    class <| "col s" ++ toString n


mcol : Int -> Attr msg
mcol n =
    class <| "col m" ++ toString n


lcol : Int -> Attr msg
lcol n =
    class <| "col l" ++ toString n


xlcol : Int -> Attr msg
xlcol n =
    class <| "col xl" ++ toString n
