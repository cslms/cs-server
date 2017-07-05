module Codeschool.Tea
    exposing
        ( Model
        , Msg
        , init
        , main
        , mainWithFlags
        , subscriptions
        , update
        , view
        )

{-| A cup of TEA :)


# Creating a new Codeschool Codeschool

-}

import Codeschool.Model as Model
import Codeschool.Msg as Msg
import Codeschool.Sub as Sub
import Codeschool.View as View
import Html exposing (Html)
import Navigation

type alias Model =
    Model.Model


type alias Msg =
    Msg.Msg


init : Model.Model
init =
    Model.init


view : Model -> Html Msg
view m =
    View.view (Html.div [] []) m


update : Msg -> Model -> ( Model, Cmd Msg )
update msg m =
    Msg.update msg m


subscriptions : Model -> Sub Msg
subscriptions model =
    Sub.subscriptions model


{-| Basic TEA for Codeschool Codeschools.
-}
main : Program Never Model Msg
main =
    Html.program
        { init = ( init, Cmd.none )
        , view = view
        , update = update
        , subscriptions = subscriptions
        }


mainWithFlags : Program String Model Msg
mainWithFlags =
    Navigation.programWithFlags Msg.OnLocationChange
        { init = \x y -> ( init, Cmd.none )
        , view = view
        , update = update
        , subscriptions = subscriptions
        }
