module Forms.JsonDecode
    exposing
        ( decodeString
        , decodeValue
        , field
        , fieldType
        , form
        , validation
        , validator
        )

import Dict
import Forms.Field as Field exposing (Field, FieldType(..), stringToType)
import Forms.Form as Form exposing (Form)
import Forms.Validation as Validation exposing (Validation(..), Validator(..))
import Forms.Value as Value exposing (Value(..), jsonDecoder)
import Json.Decode as JD exposing (Decoder, andThen, bool, fail, float, int, list, nullable, oneOf, string, succeed, value)
import Json.Decode.Pipeline as Pipeline exposing (decode, hardcoded, optional)
import Maybe


{-| Form type with string-based ids.

Used for Json serialization/deserialization.

-}
type alias JsonForm =
    Form String


{-| Field type with string-based ids.

Used for Json serialization/deserialization.

-}
type alias JsonField =
    Field String


{-| Convert JSON string to a form object
-}
decodeString : String -> Result String JsonForm
decodeString json =
    JD.decodeString form json


{-| Convert JSON value to a form object
-}
decodeValue : JD.Value -> Result String JsonForm
decodeValue json =
    JD.decodeValue form json


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
    let
        { label, required, requiredMessage, which, validators, errors, default, helpText, placeholder } =
            Field.charField ""
    in
    Pipeline.decode Field
        |> Pipeline.required "id" string
        |> optional "value" string ""
        |> optional "label" string label
        |> optional "type" fieldType which
        |> optional "required" bool required
        |> optional "requiredMessage" string requiredMessage
        |> optional "validators" (list validator) validators
        |> optional "errors" validation errors
        |> optional "default" (nullable string) default
        |> optional "helpText" (nullable string) helpText
        |> optional "placeholder" (nullable string) placeholder


{-| Decode FieldType values
-}
fieldType : Decoder FieldType
fieldType =
    let
        convert raw =
            case stringToType raw of
                Just value ->
                    succeed value

                Nothing ->
                    fail <| "invalid FieldType: '" ++ raw ++ "'."
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
