module Main exposing (..)

import Html exposing (Html, a, button, div, h1, i, li, p, span, text, ul)
import Html.Attributes exposing (class, classList, href)


-- MODEL


type alias Link =
    { text : String
    , href : String
    , alt : String
    }


type alias Section =
    { title : String
    , name : String
    , links : List Link
    }


type alias Model =
    { sections : List Section
    }



-- UTILITIES


discardSection : String -> List Section -> List Section
discardSection name sections =
    List.filter (\x -> x.name /= name) sections


link : String -> String -> Link
link text href =
    { text = text, href = href, alt = "" }


linkAlt : String -> String -> String -> Link
linkAlt text href alt =
    { text = text, href = href, alt = alt }


fillStr : String -> String -> String
fillStr str fill =
    if String.isEmpty str then
        fill
    else
        str



-- UPDATE


type Msg
    = AddSection Section
    | RemoveSection String


update : Msg -> Model -> Model
update msg model =
    case msg of
        AddSection section ->
            { sections = model.sections ++ [ section ] }

        RemoveSection name ->
            { sections = discardSection name model.sections }



-- VIEW


viewLink : Link -> Html Msg
viewLink link =
    a [ href (fillStr link.href "#") ] [ text link.text ]


viewSection : Section -> Html Msg
viewSection section =
    div []
        [ h1 [] [ text section.title ]
        , ul []
            (section.links
                |> List.map viewLink
                |> List.map (\x -> li [] [ x ])
            )
        ]


view : Model -> Html Msg
view model =
    div [] (List.map viewSection model.sections)



-- MAIN


defaultState : Model
defaultState =
    { sections =
        [ { title = "Example title"
          , name = "default"
          , links =
                [ link "link 1" "#1"
                , link "link 0" ""
                , linkAlt "link 2" "#2" "alt 2"
                ]
          }
        ]
    }


main : Program Never Model Msg
main =
    Html.beginnerProgram { model = defaultState, view = view, update = update }
