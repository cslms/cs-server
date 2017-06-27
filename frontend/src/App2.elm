module App exposing (..)

import Bootstrap.CDN as CDN
import Codeschool.Auth.ProfileEdit as ProfileEdit
import Codeschool.Page as Page
import Html exposing (Html, div, img, text)


---- MODEL ----


type alias Model =
    { page : Page.Model
    , profile : ProfileEdit.Model
    }


init : ( Model, Cmd Msg )
init =
    ( { page = Page.init
      , profile = ProfileEdit.init
      }
    , Cmd.none
    )



---- UPDATE ----


type Msg
    = NoOp
    | Page Page.Msg
    | Profile ProfileEdit.Msg


update : Msg -> Model -> ( Model, Cmd Msg )
update msg_ model =
    case msg_ of
        Page msg ->
            let
                ( page, cmd ) =
                    Page.update msg model.page
            in
            ( { model | page = page }, Cmd.map Page cmd )

        Profile msg ->
            let
                ( profile, cmd ) =
                    ProfileEdit.update msg model.profile
            in
            ( { model | profile = profile }, Cmd.map Profile cmd )

        _ ->
            ( model, Cmd.none )



---- VIEW ----


view : Model -> Html Msg
view model =
    div []
        [ CDN.stylesheet
        , Page.view Page
            model.page
            [ Html.map Profile <| ProfileEdit.view model.profile ]
        ]



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
    Sub.batch
        [ Sub.map Page <| Page.subscriptions model.page
        ]
