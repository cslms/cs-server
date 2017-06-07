module Main exposing (..)

import Html exposing (Html, a, button, div, h1, i, li, p, span, text, ul)
import Html.Attributes exposing (class, classList, href)


-- MODEL


type alias Model =
    {}



-- UPDATE


type Msg
    = Empty


update : Msg -> Model -> Model
update msg model =
    {}



-- VIEW


view : Model -> Html Msg
view model =
    div [] [ text "Hello World" ]



-- MAIN


main : Program Never Model Msg
main =
    Html.beginnerProgram { model = {}, view = view, update = update }
