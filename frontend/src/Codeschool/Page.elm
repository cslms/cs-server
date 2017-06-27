module Codeschool.Page
    exposing
        ( Model
        , Msg
        , init
        , subscriptions
        , update
        , view
        )

{-| Header element for a codechool page.

@docs Model, Msg, init, view, update, subscriptions

-}

import Codeschool.Footer as Footer
import Codeschool.Header as Header
import Html exposing (..)
import Platform.Sub as Sub


{-| Model that controls element
-}
type alias Model =
    { header : Header.Model
    , footer : Footer.Model
    }


{-| Message
-}
type Msg
    = Header Header.Msg
    | Footer Footer.Msg


{-| Start element in default state
-}
init : Model
init =
    { header = Header.init
    , footer = Footer.init
    }


{-| Update model
-}
update : Msg -> Model -> ( Model, Cmd msg )
update msg_ model =
    case msg_ of
        Header msg ->
            let
                ( header, cmd ) =
                    Header.update msg model.header
            in
            ( { model | header = header }, cmd )

        Footer msg ->
            let
                ( footer, cmd ) =
                    Footer.update msg model.footer
            in
            ( { model | footer = footer }, cmd )


{-| Renders element.
-}
view : (Msg -> msg) -> Model -> List (Html msg) -> Html msg
view wrap model main =
    let
        header =
            Header.view model.header
                |> Html.map Header
                |> Html.map wrap

        footer =
            Footer.view model.footer
                |> Html.map Footer
                |> Html.map wrap
    in
    div []
        [ div [] [ header ]
        , div [] main
        , div [] [ footer ]
        ]


{-| Subscriptions
-}
subscriptions : Model -> Sub Msg
subscriptions model =
    Sub.batch
        [ Sub.map Header <| Header.subscriptions model.header
        , Sub.map Footer <| Footer.subscriptions model.footer
        ]
