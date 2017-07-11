module Codeschool.Auth.ProfileEdit
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
import Html.Events exposing (..)
import Platform.Sub as Sub
import Forms.Form as Form exposing (FormState)


--- MODEL ---


{-| Model that controls element
-}
type alias Model =
    { section : Section
    , accountsForm : FormState 
    }


type Section
    = BasicSection
    | ChangePasswordSection
    | MessageSection
    | AccountsSection
    | DangerSection


--- UPDATE ---


{-| Start element in default state
-}
init : Model
init =
    { section = BasicSection
    , accountsForm = Form  }


{-| Update model
-}
update : Msg -> Model -> ( Model, Cmd msg )
update msg_ model =
    case msg_ of
        ChangeSection msg ->
            ( { model | section = msg }, Cmd.none )

        _ ->
            ( model, Cmd.none )



--- SUBSCRIPTIONS ---


{-| Message
-}
type Msg
    = Profile
    | NoOp
    | ChangeSection Section


{-| Subscriptions
-}
subscriptions : Model -> Sub Msg
subscriptions model =
    Sub.batch []



--- VIEW ---


{-| Renders footer element
-}
view : Model -> Html Msg
view model =
    div [ class "mdl-grid" ]
        [ navbar
        , mainForm model
        ]


cell : Int -> List (Attribute msg) -> List (Html msg) -> Html msg
cell cols attrs children =
    let
        colsClass =
            "mdl-cell--" ++ toString cols ++ "--col"

        attrs_ =
            attrs ++ [ class <| "mld-cell" ++ colsClass ]
    in
    div attrs_ children


navbar : Html Msg
navbar =
    let
        item sec x =
            li [ onClick (ChangeSection sec) ] [ text x ]
    in
    cell 4
        [ class "mdl-shadow--4dp"
        , style [ ( "padding", "15px" ) ]
        ]
        [ ul []
            [ item BasicSection "Basic information"
            , item ChangePasswordSection "Change password"

            --, item BasicSection "Message settings"
            , item AccountsSection "Accounts"
            , item DangerSection "Danger!"
            ]
        ]


mainForm : Model -> Html msg
mainForm model =
    cell 8 [] <|
        case model.section of
            BasicSection ->
                basicForm model

            ChangePasswordSection ->
                passwordForm model

            AccountsSection ->
                accountsFormView model.accounts

            DangerSection ->
                deleteAccount model

            _ ->
                []


basicForm : Model -> List (Html msg)
basicForm model =
    [ h2 [] [ text "Basic Information" ]
    , div []
        [ formInput "Full name" Nothing
        , formInput "E-mail (required)" Nothing
        , formInput "Username (required)" Nothing
        , formInput "Gender" Nothing
        , formInput "School Id" Nothing
        , formInput "Phone" Nothing
        , formInput "About Me" Nothing
        , formInput "Who can view my profile" Nothing
        ]
    ]


passwordForm : Model -> List (Html msg)
passwordForm model =
    [ h2 [] [ text "Change password" ]
    , div []
        [ formInput "Old password" Nothing
        , formInput "New password" Nothing
        , formInput "New password (again)" Nothing
        , button [] [ text "Send!" ]
        ]
    ]


deleteAccount : Model -> List (Html msg)
deleteAccount model =
    [ h2 [] [ text "Delete account" ]
    , p [] [ text "Be cautions! This operation is irriversible." ]
    , p [] [ text "Please type the text \"I want to delete my account\" in the box bellow." ]
    , div []
        [ formInput "Screte box" Nothing
        , button [] [ text "I understand. Confirm deletion" ]
        ]
    ]


formInput : String -> Maybe String -> Html msg
formInput name error =
    div [ style [ ( "padding", "20px" ) ] ]
        [ label []
            [ text name
            , input [] []
            ]
        ]
