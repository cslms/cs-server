module Forms.JsonEncode exposing (encode, toValue)

{-| This module exposes two functions, `encode` and `toValue` that are used to encode
arbitrary Forms into JSON

@docs encode, toValue

-}

import Forms.Types
    exposing
        ( Field
        , Form
        , JsonField
        , JsonForm
        , Validation(..)
        , Validator(..)
        , validatorRef
        )
import Json.Encode exposing (..)


{-| Convert form to a Json.Encode.Value object
-}
toValue : Form id -> Value
toValue form =
    toJsonForm form
        |> jsonFormtoValue


{-| Encode form into a JSON string
-}
encode : Int -> Form id -> String
encode n form =
    toValue form |> Json.Encode.encode n


toJsonForm : Form id -> JsonForm
toJsonForm form =
    { action = form.action
    , fields = List.map toJsonField form.fields
    }


toJsonField : Field id -> JsonField
toJsonField field =
    { id = toString field.id
    , value = field.value
    , label = field.label
    , inputType = field.inputType
    , default = field.default
    , helpText = field.helpText
    , placeholder = field.placeholder
    , required = field.required
    , validators = field.validators
    , errors = field.errors
    }


{-| Convert Form to JSON Value
-}
jsonFormtoValue : JsonForm -> Value
jsonFormtoValue form =
    let
        (?) : (x -> Value) -> Maybe x -> Value
        (?) enc x =
            case x of
                Nothing ->
                    null

                Just xx ->
                    enc xx

        -- Convert error to value
        error err =
            case err of
                Valid ->
                    list []

                Errors err ->
                    list <| List.map string err

        -- Convert validator to value
        validator val =
            let
                fullobject err tail =
                    let
                        head =
                            [ ( "validator", string (validatorRef val) ), ( "msg", string err ) ]
                    in
                    object <| head ++ tail

                simpleobject err =
                    fullobject err []

                valueobject err x =
                    fullobject err [ ( "value", x ) ]
            in
            case val of
                Decimal i j err ->
                    fullobject err [ ( "places", int i ), ( "size", int j ) ]

                FileExtension exts err ->
                    valueobject err (list <| List.map string exts)

                RegexMatch re err ->
                    valueobject err (string re)

                MinLength n err ->
                    valueobject err (int n)

                MaxLength n err ->
                    valueobject err (int n)

                MinValue x err ->
                    valueobject err (float x)

                MaxValue x err ->
                    valueobject err (float x)

                NotEmpty err ->
                    simpleobject err

                IsNumeric err ->
                    simpleobject err

                IsEmail err ->
                    simpleobject err

                IsURL err ->
                    simpleobject err

        -- Convert field to value
        field : JsonField -> Value
        field f =
            object
                [ ( "id", string <| String.toLower f.id )
                , ( "value", string f.value )
                , ( "label", string f.label )
                , ( "inputType", string (toString f.inputType |> String.toLower) )
                , ( "required", bool f.required )
                , ( "validators", list <| List.map validator f.validators )
                , ( "errors", error f.errors )

                -- TODO: should we ommit empty values?
                , ( "default", string ? f.default )
                , ( "helpText", string ? f.helpText )
                , ( "placeholder", string ? f.placeholder )
                ]
    in
    object
        [ ( "action", string ? form.action )
        , ( "fields", list (List.map field form.fields) )
        ]
