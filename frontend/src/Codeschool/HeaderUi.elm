module Codeschool.HeaderUi
    exposing
        ( Model
        , Msg
        , init
        , subscriptions
        , update
        , view
        )

{-| Header element for a codechool page.

@docs Model, init, view, update, subscriptions

-}

import Html exposing (..)
import Html.Attributes exposing (..)
import Platform.Sub as Sub
import Ui.DropdownMenu
import Ui.Helpers.Dropdown as Dropdown exposing (..)


{-| Model that contros header state
-}
type alias Model =
    { userDropdown : Ui.DropdownMenu.Model }


{-| Message
-}
type Msg
    = Dropdown Ui.DropdownMenu.Msg


{-| Start header elment in default state
-}
init : Model
init =
    { userDropdown =
        Ui.DropdownMenu.init ()
    }


{-| Update model
-}
update : Msg -> Model -> ( Model, Cmd msg )
update msg_ model =
    case msg_ of
        Dropdown msg ->
            let
                menu =
                    Ui.DropdownMenu.update msg model.userDropdown
            in
            ( { model | userDropdown = menu }, Cmd.none )


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
    let
        config =
            { items =
                [ ul [ class "mdl-list" ]
                    [ mdlMenuItem [ text "foo" ]
                    , mdlMenuItem [ text "bar" ]
                    ]
                ]
            , element =
                span [ class "cs-head__fab mdl-button mdl-js-button mdl-button--fab mdl-button--colored fab-button", id "cs-head--dropdown-trigger" ]
                    [ span [ class "dropdown-trigger" ]
                        [ i [ class "material-icons" ] [ text "person_outline" ] ]
                    ]
            , address = Dropdown
            }
    in
    Ui.DropdownMenu.view config model.userDropdown


mdlMenuItem children =
    li [ class "mdl-list__item" ] children


{-| Subscriptions
-}
subscriptions : Model -> Sub Msg
subscriptions model =
    Sub.map Dropdown <| Ui.DropdownMenu.subscriptions model.userDropdown
