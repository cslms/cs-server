module Main exposing (..)

import Html


main =
    Html.beginnerProgram
        { model = "Hello World"
        , view = \m -> Html.p [] [Html.text m]
        , update = \m msg -> m 
        }
