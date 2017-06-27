module Codeschool.Header
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

import Codeschool.Utils exposing (icon, iconAttrs)
import Html exposing (..)
import Html.Attributes exposing (..)
import Platform.Sub as Sub


{-| Model that contros header state
-}
type alias Model =
    { menuDown : Bool }


{-| Message
-}
type Msg
    = Menu Bool


{-| Start header elment in default state
-}
init : Model
init =
    { menuDown = True
    }


{-| Update model
-}
update : Msg -> Model -> ( Model, Cmd msg )
update msg_ model =
    case msg_ of
        Menu state ->
            ( { model | menuDown = not state }, Cmd.none )


{-| View header component.
-}
view : Model -> Html Msg
view model =
    div [ class "cs-head mdl-cell mdl-cell--12-col" ]
        [ div [ class "cs-logo" ]
            [ div [ class "cs-logo__img" ]
                []
            ]
        , nav [ class "cs-head__nav" ]
            [ div [ class "cs-head__links" ]
                [ a [ href "/questions/" ]
                    [ text "Questions" ]
                ]
            , viewFabButton model
            ]
        ]


viewFabButton : Model -> Html Msg
viewFabButton model =
    div []
        [ span
            [ class "cs-head__fab mdl-button mdl-button--fab mdl-button--colored fab-button active"
            ]
            [ span [ class "dropdown-trigger is-visible" ]
                [ icon "person_outline" ]
            ]
        , ul
            [ class "mdl-menu mdl-menu--bottom-left is-visible"
            ]
            [ menuItem
                [ a [ href "/auth/chips" ]
                    [ text "Profile" ]
                ]
            , menuItem
                [ a [ href "/auth/logout/" ]
                    [ text "Logout" ]
                ]
            ]
        ]


menuItem : List (Html msg) -> Html msg
menuItem children =
    li [ class "mdl-menu__item" ] children


{-| Subscriptions
-}
subscriptions : Model -> Sub Msg
subscriptions model =
    Sub.batch []
