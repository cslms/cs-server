module Bricks.Serializer exposing (Brick)

{-|


# Brick Serializer


# Types

@docs Brick

-}

import Html exposing (..)
import Html.Attributes as Attr exposing (..)
import Json.Decode as Json exposing (Decoder, andThen, field, index, list, map3, string)


{-| Respresent a brick HTML element without actually constructing that element
-}
type alias Brick =
    { tag : String
    , attrs : List ( String, String )
    , children : Children
    }


type Children
    = Children (List Brick)



-- CONSTRUCTORS


{-| Create a brick from tag name, arguments and children
-}
brick : String -> List ( String, String ) -> List Brick -> Brick
brick tag attrs children =
    { tag = tag, attrs = attrs, children = Children children }



-- PROPERTIES


children : Brick -> List Brick
children brick =
    case brick.children of
        Children lst ->
            lst



-- VIEWS


{-| Render brick into an Html msg element
-}
render : Brick -> Html msg
render brick =
    let
        elem =
            tagToHtml brick.tag

        childrenList =
            children brick

        attrs_ =
            List.map attrToAttribute brick.attrs
    in
    elem [] <| List.map render childrenList


tagToHtml : String -> (List (Attribute msg) -> List (Html msg) -> Html msg)
tagToHtml tag =
    case tag of
        "a" ->
            a

        _ ->
            div


attrToAttribute : ( String, String ) -> Attribute msg
attrToAttribute ( attr, value ) =
    case attr of
        "id" ->
            Attr.id value

        a ->
            Attr.attribute a value



-- JSON DECODING


brickDecoder : Decoder Brick
brickDecoder =
    map3 Brick
        (field "tag" string)
        (field "attrs" <| Json.list <| tupleDecoder2 ( string, string ))
        (field "children" childrenDecoder)


childrenDecoder : Decoder Children
childrenDecoder =
    Json.map Children (Json.list (Json.lazy (\_ -> brickDecoder)))


tupleDecoder2 : ( Decoder a, Decoder b ) -> Decoder ( a, b )
tupleDecoder2 ( a, b ) =
    index 0 a
        |> andThen
            (\a_ ->
                index 1 b
                    |> andThen (\b_ -> Json.succeed ( a_, b_ ))
            )


{-| Create a Brick element from Json
-}
fromJson : String -> Result String Brick
fromJson data =
    Json.decodeString brickDecoder data
