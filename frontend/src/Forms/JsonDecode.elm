module Forms.JsonDecode exposing (form, fromJson)

import Dict
import Forms.Types
    exposing
        ( Field
        , Form
        , InputType
        , JsonField
        , JsonForm
        , stringToInputType
        )
import Forms.Validation as Validation exposing (Validation(..), Validator(..))
import Forms.Value as Value exposing (Value(..), jsonDecoder)
import Json.Decode as JD exposing (Decoder, andThen, bool, fail, float, int, list, nullable, oneOf, string, succeed, value)
import Json.Decode.Pipeline as Pipeline exposing (decode, hardcoded, optional, required)
import Maybe


{-| Convert JSON value to a form object
-}
fromJson : String -> Result String JsonForm
fromJson json =
    JD.decodeString form json


{-| Decode JsonForm (Form String) objects
-}
form : Decoder JsonForm
form =
    JD.map2 Form
        (JD.field "action" (nullable string))
        (JD.field "fields" (list field))


{-| Decode JsonField (Field String) objects
-}
field : Decoder JsonField
field =
    Pipeline.decode Field
        |> required "id" string
        |> optional "value" string ""
        |> optional "label" string "Input"
        |> optional "inputType" inputType Forms.Types.Text
        |> optional "required" bool True
        |> optional "validators" (list validator) []
        |> optional "errors" validation Valid
        |> optional "default" (nullable string) Nothing
        |> optional "helpText" (nullable string) Nothing
        |> optional "placeholder" (nullable string) Nothing


{-| Decode InputType values
-}
inputType : Decoder InputType
inputType =
    let
        convert raw =
            case stringToInputType raw of
                Just value ->
                    succeed value

                Nothing ->
                    fail <| "invalid input type: '" ++ raw ++ "'."
    in
    string |> andThen convert


{-| Decode Validator values
-}
validator : Decoder Validator
validator =
    let
        convert : List ( String, Value ) -> Decoder Validator
        convert x =
            let
                dic =
                    Dict.fromList x

                name =
                    Dict.get "validator" dic
                        |> Maybe.withDefault (String "")
                        |> Value.toString

                msg =
                    Dict.get "msg" dic
                        |> Maybe.withDefault (String "Error")
                        |> Value.toString

                opts : List ( String, Value )
                opts =
                    dic
                        |> Dict.remove "validator"
                        |> Dict.remove "msg"
                        |> Dict.toList

                optsList =
                    opts
                        |> List.map (\( x, y ) -> ( x, Value.toString y ))

                val =
                    Validation.fromInfo ( name, msg, opts )
            in
            case val of
                Ok x ->
                    succeed x

                Err _ ->
                    fail ("invalid validator: " ++ toString x)
    in
    JD.keyValuePairs jsonDecoder |> andThen convert


{-| Decode Validation results
-}
validation : Decoder Validation
validation =
    let
        convert raw =
            case raw of
                Just errors ->
                    succeed (Errors errors)

                Nothing ->
                    succeed Valid
    in
    nullable (list string) |> andThen convert



--- CONSTRUCTOR FOR DEFAULT JSON OBJECTS ---


jsonForm : JsonForm
jsonForm =
    { action = Nothing, fields = [] }


jsonField : JsonField
jsonField =
    { id = ""
    , value = ""
    , label = "Input"
    , inputType = Forms.Types.Text
    , helpText = Nothing
    , required = False
    , placeholder = Nothing
    , default = Nothing
    , validators = []
    , errors = Valid
    }
