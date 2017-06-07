module Main exposing (..)

import Html exposing (Html, a, button, div, h1, i, p, span, text)
import Html.Attributes exposing (class, classList, href)


-- MODEL


type alias Model =
    { title : String
    , text : String
    , icon : String
    , href : String
    , faded : Bool
    }



-- UPDATE


type Msg
    = Increment
    | Decrement


update : Msg -> Model -> Model
update msg model =
    model



-- VIEW


simpleIcon : String -> Html Msg
simpleIcon icon =
    i [ class "material-design-icon cs-card__icon" ] [ text icon ]


cardIcon : Model -> Html Msg
cardIcon model =
    if String.isEmpty model.icon then
        simpleIcon "help"
    else if String.isEmpty model.href then
        simpleIcon model.icon
    else
        a [ href model.href, class "cs-card__link" ] [ simpleIcon model.icon ]


view : Model -> Html Msg
view model =
    div
        [ classList
            [ ( "cs-card", True )
            , ( "mdl-shadow--4dp", True )
            , ( "mdl-cell", True )
            , ( "cs-card--faded", model.faded )
            ]
        ]
        [ cardIcon model
        , h1 [ class "cs-card__title" ] [ text model.title ]
        , p [] [ text model.text ]
        ]



-- MAIN


defaultState : Model
defaultState =
    { title = "Card title"
    , text = "Card text"
    , href = ""
    , icon = "help_circle"
    , faded = False
    }


initialState : Model
initialState =
    { defaultState | title = "Example", text = "text" }


main : Program Never Model Msg
main =
    Html.beginnerProgram { model = initialState, view = view, update = update }
