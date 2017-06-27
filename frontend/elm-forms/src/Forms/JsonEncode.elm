module Forms.JsonEncode exposing (encode, toValue)

{-| This module exposes two functions, `encode` and `toValue` that are used to encode
arbitrary Forms into JSON

@docs encode, toValue

-}

import Forms.Field exposing (Field)
import Forms.Form exposing (Form)
import Forms.Validation exposing (Validation(..), Validator(..), validatorInfo)
import Json.Encode exposing (..)


--- TYPE ALIASES ---


type alias JsonForm =
    Form String


type alias JsonField =
    Field String



--- CONVERTERS ---


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
    , which = field.which
    , default = field.default
    , helpText = field.helpText
    , placeholder = field.placeholder
    , required = field.required
    , requiredMessage = field.requiredMessage
    , validators = field.validators
    , errors = field.errors
    }


{-| Convert Form to JSON Value
-}
jsonFormtoValue : JsonForm -> Value
jsonFormtoValue form =
    let
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
                        ( ref, _, _ ) =
                            validatorInfo val

                        head =
                            [ ( "validator", string ref ), ( "msg", string err ) ]
                    in
                    object <| head ++ tail

                simpleobject err =
                    fullobject err []

                valueobject err value =
                    fullobject err [ ( "value", value ) ]
            in
            case val of
                -- Decimal i j err ->
                --     fullobject err [ ( "places", int i ), ( "size", int j ) ]
                -- FileExtension exts err ->
                --     valueobject err (list <| List.map string exts)
                -- RegexMatch re err ->
                --     valueobject err (string re)
                -- NotEmpty err ->
                --     simpleobject err
                -- IsNumeric err ->
                --     simpleobject err
                -- IsEmail err ->
                --     simpleobject err
                -- IsURL err ->
                --     simpleobject err
                MinLength err { value } ->
                    valueobject err (int value)

                MaxLength err { value } ->
                    valueobject err (int value)

                MinValue err { value } ->
                    valueobject err (float value)

                MaxValue err { value } ->
                    valueobject err (float value)

        -- Convert field to value
        field : JsonField -> Value
        field f =
            object
                [ ( "id", string <| String.toLower f.id )
                , ( "value", string f.value )
                , ( "label", string f.label )
                , ( "type", string (toString f.which |> String.toLower) )
                , ( "required", bool f.required )
                , ( "requiredMessage", string f.requiredMessage )
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


(?) : (x -> Value) -> Maybe x -> Value
(?) enc x =
    case x of
        Nothing ->
            null

        Just xx ->
            enc xx
