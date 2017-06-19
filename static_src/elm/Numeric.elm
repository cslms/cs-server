module Main exposing (..)

import Codeschool.Navbar as Navbar exposing (..)
import Codeschool.User as User exposing (User)
import Dialog
import Html exposing (..)
import Html.Attributes exposing (..)
import Html.Events exposing (..)
import Markdown
import Maybe
import String


-- MODEL


type alias Model =
    { question : Question
    , user : User
    , response : Response
    , showModal : Bool
    , showNavbar : Bool
    }


type alias Response =
    { value : Maybe Float
    , feedback : Feedback
    }


type Feedback
    = Error String
    | Waiting
    | Empty


type alias Question =
    { title : String
    , shortDescription : String
    , longDescription : List DescriptionItem
    }


{-| Type of each node of a Stream field and its corresponding contents
-}
type DescriptionItem
    = Markdown String
    | Html String
    | Ignored


model : Model
model =
    { user = User.fake
    , question = emptyQuestion
    , response = { value = Nothing, feedback = Empty }
    , showModal = False
    , showNavbar = True
    }


emptyQuestion : Question
emptyQuestion =
    { title = "The Answer"
    , shortDescription = "Life the universe and everything"
    , longDescription = [ Markdown "What is the answer?" ]
    }



-- ACTION, UPDATE


type Msg
    = SetResponse String
    | SubmitResponse
    | CloseModal
    | NavbarMsg



-- Boilerplate: Msg clause for internal Mdl messages.


feedback : Maybe Float -> Feedback
feedback value =
    case value of
        Nothing ->
            Error "Empty string!"

        _ ->
            Waiting


update : Msg -> Model -> Model
update msg ({ response } as model) =
    case msg of
        SetResponse value ->
            let
                number =
                    if String.isEmpty value then
                        Nothing
                    else
                        case String.toFloat value of
                            Ok num ->
                                Just num

                            Err _ ->
                                Nothing
            in
            { model | response = { response | value = number } }

        SubmitResponse ->
            { model
                | response = { response | feedback = feedback response.value }
                , showModal = True
            }

        CloseModal ->
            { model | showModal = False }

        _ ->
            model



-- VIEW


showDialog : String -> String -> Html Msg
showDialog title msg =
    Dialog.render
        { styles = [ ( "class", "cs-dialog" ) ]
        , title = title
        , content = [ p [] [ text msg ] ]
        , actionBar =
            [ button [ class "mdl-button", onClick CloseModal ] [ text "Close" ]
            ]
        }
        Dialog.visible


showFeedbackDialog : Feedback -> Html Msg
showFeedbackDialog feedback =
    case feedback of
        Error msg ->
            showDialog "Error" msg

        Waiting ->
            showDialog "Waiting..." "Please wait while codeschool grade your submission"

        _ ->
            showDialog "" ""


view : Model -> Html Msg
view ({ question, user, response, showModal } as model) =
    let
        modal =
            if showModal then
                [ showFeedbackDialog response.feedback ]
            else
                []

        head_ =
            [ header
            , div
                [ id "cs-body"
                , class "mdl-grid mdl-grid mdl-grid--no-spacing"
                , style [ ( "width", "100%" ) ]
                ]
                [ div [ id "content-area", class "cs-stripes-layout" ]
                    [ Navbar.render model.showNavbar, contents question ]
                ]
            ]
    in
    div [ class "cs-base-page", attribute "unresolved" "unresolved" ]
        (head_ ++ modal ++ [ footer ])


header : Html Msg
header =
    div [ class "cs-head mdl-cell mdl-cell--12-col" ]
        [ div [ class "cs-logo" ]
            [ img [ class "cs-logo__img", src "/static/img/logo.svg" ]
                []
            ]
        , nav [ class "cs-head__nav" ]
            [ div [ class "cs-head__links" ]
                [ a [ href "/questions/" ]
                    [ text "Questions" ]
                ]
            , span [ class "cs-head__fab mdl-button mdl-js-button mdl-button--fab mdl-button--colored fab-button", id "cs-head--dropdown-trigger" ]
                [ span [ class "dropdown-trigger" ]
                    [ text "a" ]
                ]
            , ul [ class "mdl-menu mdl-menu--bottom-left mdl-js-menu mdl-js-ripple-effect", for "cs-head--dropdown-trigger" ]
                [ li [ class "mdl-menu__item" ]
                    [ a [ href "/profile/" ]
                        [ text "Profile" ]
                    ]
                , li [ class "mdl-menu__item" ]
                    [ a [ href "/auth/logout/" ]
                        [ text "Logout" ]
                    ]
                ]
            ]
        ]


footer : Html Msg
footer =
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


{-| Displays the content header title and subtitle.
-}
contentHeader : String -> String -> Html Msg
contentHeader title subtitle =
    div []
        [ h1 []
            [ text title ]
        , p []
            [ text
                (if String.isEmpty subtitle then
                    title
                 else
                    subtitle
                )
            ]
        ]


longDescription : List DescriptionItem -> Html Msg
longDescription data =
    let
        description : DescriptionItem -> Html Msg
        description item =
            case item of
                Markdown md ->
                    Markdown.toHtml [ class "cs-markdown" ] md

                Html x ->
                    div [] [ text x ]

                Ignored ->
                    span [] []
    in
    div []
        [ h2 [ class "cs-banner" ]
            [ text "Description" ]
        , article [ class "question-stem" ] <|
            List.map description data
        ]


numericInput : Html Msg
numericInput =
    section []
        [ h2 [ class "cs-banner" ] [ text "Response" ]
        , div []
            [ label []
                [ text "Answer:"
                , input
                    [ step "any"
                    , type_ "number"
                    , placeholder "type your answer here"
                    , onInput SetResponse
                    ]
                    []
                ]
            ]
        , div [ class "toolbar highlight", style [ ( "text-align", "right" ), ( "margin-top", "20px" ) ] ]
            [ button
                [ class "mdl-button mdl-js-button mdl-button--raised"
                , attribute "form" "form"
                , onClick SubmitResponse
                ]
                [ text "Enviar" ]
            ]
        ]


contents : Question -> Html Msg
contents question =
    main_ [ class "cs-stripes-layout__main" ]
        [ div [ class "cs-stripes-layout__content" ]
            [ contentHeader question.title question.shortDescription
            , div []
                [ longDescription question.longDescription
                , numericInput
                ]
            ]
        ]


main : Program Never Model Msg
main =
    Html.beginnerProgram
        { model = model
        , view = view
        , update = update
        }
