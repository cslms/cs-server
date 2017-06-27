module Codeschool.Footer
    exposing
        ( Model
        , Msg
        , init
        , subscriptions
        , update
        , view
        )

{-| Footer element for a codechool page.

@docs Model, Msg, init, view, update, subscriptions

-}

import Html exposing (..)
import Html.Attributes exposing (..)
import Platform.Sub as Sub


{-| Model that controls element
-}
type alias Model =
    {}


{-| Message
-}
type Msg
    = Footer


{-| Start element in default state
-}
init : Model
init =
    {}


{-| Update model
-}
update : Msg -> Model -> ( Model, Cmd msg )
update msg_ model =
    ( model, Cmd.none )


{-| Renders footer element
-}
view : Model -> Html msg
view model =
    div [ class "cs-foot mdl-cell mdl-cell--12-col" ]
        [ div [ class "cs-foot__copyright" ]
            [ p []
                [ text "Copyright 2016 -"
                , a
                    [ href "http://github.com/fabiommendes/codeschool" ]
                    [ text "Codeschool" ]
                ]
            , p []
                [ text "Site gerenciado por Fábio M. Mendes na UnB/Gama." ]
            ]
        ]


{-| Subscriptions
-}
subscriptions : Model -> Sub Msg
subscriptions model =
    Sub.batch []