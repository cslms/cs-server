module App exposing (..)

import Forms.Form as Form exposing (Form, FormMsg)
import Forms.JsonDecode as Decode exposing (decodeString)
import Html exposing (Html, code, div, h2, pre, text)
import Html.Attributes exposing (style)
import Json.Decode exposing (Value)
import Debug


--- Form ---


type alias Model =
    Form String


json =
    """{
    "action": null,
    "fields": [
        {
            "id": "username",
            "value": "",
            "label": "E-mail",
            "type": "email",
            "required": true,
            "validators": [],
            "errors": [],
            "default": null,
            "helpText": null,
            "placeholder": "Enter your e-mail"
        },
        {
            "id": "password",
            "value": "",
            "label": "Password",
            "type": "password",
            "required": true,
            "validators": [],
            "errors": [],
            "default": null,
            "helpText": null,
            "placeholder": "Enter your password"
        }
    ]
}
"""



---- UPDATE ----


type alias Msg
    = FormMsg String


update : Msg -> Model -> ( Model, Cmd Msg )
update msg form =
    ( Form.update msg form, Cmd.none )



---- VIEW ----


view : Model -> Html Msg
view model =
    div [ style [ ( "width", "500px" ), ( "margin", "auto auto" ) ] ]
        [ h2 [] [ text "Form" ]
        , Form.view model
        ]



---- PROGRAM ----


main : Program Value Model Msg
main =
    let
        model =
            case decodeString json of
                Ok x ->
                    Debug.log "decode" x

                Err err ->
                    Debug.log (err) Form.form [] []
    in
    Html.programWithFlags
        { view = view
        , init = \flags -> ( model, Cmd.none )
        , update = update
        , subscriptions = subscriptions
        }



-- SUBSCRIPTIONS


subscriptions : Model -> Sub Msg
subscriptions model =
    Sub.batch []
