module Codeschool.Main
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

{-| Codeschool main application. It orchestrates all functions in the elm
archtechiture and provides both main and mainWithFlags.
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


{-| Init codeschool model
-}
init : Model.Model
init =
    Model.init


{-| A view function for the site
-}
view : Model -> Html Msg
view m =
    View.view (Html.div [] []) m


{-| Main update function for Codeschool.Msg types.
-}
update : Msg -> Model -> ( Model, Cmd Msg )
update msg m =
    Msg.update msg m


{-| Register Codeschool's subscriptions
-}
subscriptions : Model -> Sub Msg
subscriptions model =
    Sub.subscriptions model


{-| Basic TEA main function for Codeschool pages.
-}
main : Program Never Model Msg
main =
    Html.program
        { init = ( init, Cmd.none )
        , view = view
        , update = update
        , subscriptions = subscriptions
        }


{-| A main function that receives an URL route flag from Javscript.
-}
mainWithFlags : Program String Model Msg
mainWithFlags =
    Navigation.programWithFlags Msg.ChangeLocation
        { init = \x y -> ( init, Cmd.none )
        , view = view
        , update = update
        , subscriptions = Sub.subscriptions
        }
