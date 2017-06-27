module Forms.Value
    exposing
        ( Value(..)
        , fromJson
        , isEmpty
        , jsonDecoder
        , nCmp
        , toBool
        , toFloat
        , toInt
        , toJson
        , toString
        )

{-| A dynamic type that tracks JSON-compatible types
-}

import Basics
import Json.Decode as Jd exposing (andThen, fail, succeed)
import Json.Encode as Je


{-| Basic type representing the content of a field
-}
type Value
    = Empty
    | String String
    | Int Int
    | Bool Bool
    | Float Float
    | List (List Value)



--- CONVERTERS ---


{-| Extract value as a string
-}
toString : Value -> String
toString v =
    case v of
        Empty ->
            ""

        String st ->
            st

        Float x ->
            Basics.toString x

        Int x ->
            Basics.toString x

        Bool x ->
            case x of
                True ->
                    "true"

                False ->
                    "false"

        List x ->
            Basics.toString <| List.map toString x


{-| Extract a float result from value
-}
toFloat : Value -> Result String Float
toFloat v =
    case v of
        Float x ->
            Ok x

        Int x ->
            Ok (Basics.toFloat x)

        _ ->
            Err "value is not numeric"


{-| Extract an integer result from value
-}
toInt : Value -> Result String Int
toInt v =
    case v of
        Float x ->
            Ok (Basics.truncate x)

        Int x ->
            Ok x

        _ ->
            Err "value is not numeric"


{-| Convert to boolean. All non-boolean values are true-y and only
(Bool False) and Empty are falsey
-}
toBool : Value -> Bool
toBool v =
    case v of
        Empty ->
            False

        Bool x ->
            x

        _ ->
            True


{-| Convert data to Json.Encode.Value
-}
toJson : Value -> Je.Value
toJson v =
    case v of
        Empty ->
            Je.null

        String x ->
            Je.string x

        Float x ->
            Je.float x

        Int x ->
            Je.int x

        Bool x ->
            Je.bool x

        List xs ->
            Je.list (List.map toJson xs)


{-| Convert back from a Json.Encode.Value
-}
fromJson : Jd.Value -> Result String Value
fromJson v =
    Jd.decodeValue jsonDecoder v


{-| A decoder to Value types
-}
jsonDecoder : Jd.Decoder Value
jsonDecoder =
    let
        succ f =
            \x -> succeed (f x)

        listdec : List Jd.Value -> Jd.Decoder Value
        listdec =
            \x ->
                let
                    lst : List (Result String Value)
                    lst =
                        List.map (Jd.decodeValue jsonDecoder) x

                    reducer : Result String Value -> Result String (List Value) -> Result String (List Value)
                    reducer x y =
                        case ( x, y ) of
                            ( Ok a, Ok b ) ->
                                Ok (a :: b)

                            _ ->
                                Err "invalid element"

                    result : Result String (List Value)
                    result =
                        List.foldl reducer (Ok []) lst
                in
                case result of
                    Ok xs ->
                        Jd.succeed (List xs)

                    Err _ ->
                        Jd.fail "not a list"
    in
    Jd.oneOf
        [ Jd.string |> andThen (succ String)
        , Jd.float |> andThen (succ Float)
        , Jd.int |> andThen (succ Int)
        , Jd.bool |> andThen (succ Bool)
        , Jd.list Jd.value |> andThen listdec
        , Jd.null Empty
        ]



--- COMPARISONS ---


{-| Checks if value is empty
-}
isEmpty : Value -> Bool
isEmpty v =
    case v of
        String st ->
            String.isEmpty st

        Empty ->
            True

        List ls ->
            List.length ls == 0

        _ ->
            False


{-| Used to compare numeric values with Value objects:

    if nCmp x (<) 42 then
        "Value is smaller than 42"
    else
        "Value is larger than 42"

-}
nCmp : Value -> (Float -> number -> Bool) -> number -> Bool
nCmp v op num =
    case v of
        Int x ->
            op (Basics.toFloat x) num

        Float x ->
            op x num

        _ ->
            False
