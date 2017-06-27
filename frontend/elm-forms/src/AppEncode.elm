module App exposing (..)

import Forms.Contrib.LoginForm exposing (..)
import Forms.Form as Form
import Forms.JsonEncode exposing (encode)
import Html exposing (Html, code, div, h2, pre, text)
import Html.Attributes exposing (style)
import Json.Decode exposing (Value)


--- Form ---


type alias Model =
    LoginForm


init : ( Model, Cmd Msg )
init =
    ( loginByEmail, Cmd.none )



---- UPDATE ----


type Msg
    = LoginFormMsg LoginFormMsg


update : Msg -> Model -> ( Model, Cmd Msg )
update msg_ form =
    case msg_ of
        LoginFormMsg msg ->
            ( Form.update msg form, Cmd.none )



---- VIEW ----


view : Model -> Html Msg
view model =
    div [ style [ ( "width", "500px" ), ( "margin", "auto auto" ) ] ]
        [ h2 [] [ text "Second form" ]
        , Html.map LoginFormMsg (Form.view model)
        , h2 [] [ text "Form as Json" ]
        , pre [] [ text (encode 4 model) ]
        ]



---- PROGRAM ----


main : Program Value Model Msg
main =
    Html.programWithFlags
        { view = view
        , init = \flags -> init
        , update = update
        , subscriptions = subscriptions
        }



-- SUBSCRIPTIONS


subscriptions : Model -> Sub Msg
subscriptions model =
    Sub.batch []
