module App exposing (..)

import Forms.Contrib exposing (..)
import Forms.Fields exposing (..)
import Forms.Form as Form exposing (..)
import Forms.JsonDecode exposing (..)
import Forms.Validation exposing (..)
import Forms.Types exposing (..)
import Html exposing (Html, code, div, h2, pre, text)
import Html.Attributes exposing (style)


--- Form ---


type alias Model =
    { userForm : UserForm
    , loginForm : LoginForm
    }


type Fields
    = Email
    | Password
    | FullText
    | Float


type alias UserForm =
    Form Fields


formstr : String
formstr =
    """
{
    "action": "/foo/bar",
    "fields": [
        {
            "id": "name",
            "value": "name",
            "label": "Name",
            "helpText" : "Username or password",
            "inputType": "text"
        },
        {
            "id": "password",
            "value": "password",
            "label": "Password",
            "inputType": "password"
        }
    ]
}
"""


init : ( Model, Cmd Msg )
init =
    ( { userForm = loginForm, loginForm = loginByEmail }, Cmd.none )


loginForm : UserForm
loginForm =
    Form.form [ action "/api/form/1" ]
        [ charField Email
            |> label "Username or e-mail"
            |> default "user"
            |> helpText "Do something new"
        , floatField Float
            |> label "Number"
            |> placeholder "some number"
            |> validator (maxValue 10 "Value must be smaller than 10")
        , passwordField Password
            |> label "Password"
            |> placeholder "1234"
        , textField FullText
            |> label "Code"
            |> placeholder "enter your code here"
        ]



---- UPDATE ----


type Msg
    = NoOp
    | Form (FormMsg Fields)
    | LoginForm LoginFormMsg
    | JsonFormMsg (FormMsg String)


update : Msg -> Model -> ( Model, Cmd Msg )
update msg_ form =
    case msg_ of
        Form msg ->
            let
                data =
                    updateForm msg form.userForm
            in
            ( { form | userForm = data }, Cmd.none )

        _ ->
            ( form, Cmd.none )



---- VIEW ----


view : Model -> Html Msg
view model =
    let
        tail : List (Html Msg)
        tail =
            case fromJson formstr of
                Ok res ->
                    [ Html.map JsonFormMsg <| div [] [ viewForm res ] ]

                Err _ ->
                    []

        head : List (Html Msg)
        head =
            [ h2 [] [ text "First form" ]
            , Html.map Form <| viewForm model.userForm
            , h2 [] [ text "Second form" ]
            , Html.map LoginForm <| viewForm model.loginForm
            ]
    in
    div [ style [ ( "width", "500px" ), ( "margin", "auto auto" ) ] ]
        (head ++ tail)
    --div [] [ text "hello world" ]



---- PROGRAM ----


main : Program String Model Msg
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
