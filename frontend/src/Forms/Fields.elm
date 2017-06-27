module Forms.Fields
    exposing
        ( addError
        , addErrors
        , charField
        , default
        , label
        , passwordField
        , placeholder
        , required
        , resetErrors
        , setValue
        , textField
        , update
        , validate
        , view
        , helpText
        )
        -- , urlField
        -- , monthField
        -- , booleanField
        -- , colorField
        -- , dateField
        -- , datetimeField
        -- , emailField
        -- , floatField
        -- , integerField
        -- , searchField
        -- , weekField

{-| Forms.Fields defines field types and related functions. All forms and
fields have separate State and Config objects.


# Field constructors

Fields are initialized by calling a base constructor and then piping some modifiers

    charField "username"
        |> label "Username or E-mail"
        |> helpText "Type your login name or e-mail"
        |> required


@docs charField, textField, passwordField

    (not implemented yet...):

        searchField, booleanField
        emailField, urlField, floatField, integerField, dateField, monthField
        weekField, datetimeField, colorField


## Constructor modifiers

These modifiers are usually used during Field declaration as shown in the example above

@docs label, default, helpText, placeholder, required, validator


# Other field modifiers

The are setter functions usually called during the field lifecycle

@docs setValue, addError, addErrors, resetErrors


# TEA functions

@docs view, update


# Validation

@docs validate

-}

import Forms.Validation exposing (Validation(..), Validator, validateBatch)
import Html exposing (..)
import Html.Attributes as Attrs exposing (..)
import Html.Events exposing (..)
import Dict 

-------------------------------------------------------------------------------
---                             MAIN TYPES                                  ---
-------------------------------------------------------------------------------

{-| Represents a field in a form
-}
type alias Field id =
    { id : id
    , value : String
    , label : String
    , which : FieldType
    , required : Bool
    , validators : List Validator
    , errors : Validation
    , default : Maybe String
    , helpText : Maybe String
    , placeholder : Maybe String
    }
    
--- Default values
init : id -> Field id
init id =
    { id = id
    , which = Text
    , value = ""
    , label = "Input"
    , helpText = Nothing
    , required = False
    , placeholder = Nothing
    , default = Nothing
    , validators = []
    , errors = Valid
    }



{-| Html form input types
-}
type FieldType
    = Text
    | Password
    | TextArea



-- | Button
-- | Checkbox
-- | Submit
-- | File
-- | Reset
-- | Hidden
-- | Search
-- | Email
-- | Url
-- | Tel
-- | Number
-- | Range
-- | Color
-- | Date
-- | Month
-- | Week
-- | Time
-- | Datetime
-- | DatetimeLocal


{-| Convert FieldTypes to string representation
-}
typeToString : FieldType -> String
typeToString tt =
    toString tt |> String.toLower


{-| Convert strings to FieldTypes
-}
stringToType : String -> Maybe FieldType
stringToType raw =
    let
        types =
            [ Text, TextArea, Password ]

        -- ++ [ Button, Checkbox, Submit, File, Reset, Hidden ]
        -- ++ [ Search, Email, Url, Tel, Number, Range, Color ]
        -- ++ [ Date, Month, Week, Time, Datetime, DatetimeLocal ]
        strings =
            List.map typeToString types

        dict =
            Dict.fromList (List.map2 (\x y -> ( x, y )) strings types)
    in
    Dict.get raw dict


-------------------------------------------------------------------------------
---      CONSTRUCTORS: functions used to define basic field types           ---
-------------------------------------------------------------------------------


(#) : Field id -> FieldType -> Field id 
(#) x y =
    {x | which = y}

{-| A field type that renders a text area
-}
textField : id -> Field id
textField id =
    charField id # TextArea


{-| Declares a field that receives simple text input
-}
charField : id -> Field id
charField id =
    init id # Text


{-| A field that hides password inputs.
-}
passwordField : id -> Field id
passwordField id =
    charField id # Password



-- {-| A field that exhibit a search box.
-- -}
-- searchField : id -> Field id
-- searchField id =
--     charField id |> fieldType Search
-- {-| A boolean field with a checkbox.
-- -}
-- booleanField : id -> Field id
-- booleanField id =
--     charField id |> fieldType Checkbox
-- {-| A field for e-mail input.
-- -}
-- emailField : id -> Field id
-- emailField id =
--     charField id |> fieldType Email
-- {-| A field for e-mail input.
-- -}
-- urlField : id -> Field id
-- urlField id =
--     charField id |> fieldType Url
-- {-| A field for float inputs.
-- -}
-- floatField : id -> Field id
-- floatField id =
--     charField id |> fieldType Number
-- {-| A field for integer inputs.
-- -}
-- integerField : id -> Field id
-- integerField id =
--     charField id |> fieldType Number
-- {-| A field for date inputs.
-- -}
-- dateField : id -> Field id
-- dateField id =
--     charField id |> fieldType Date
-- {-| A field for month inputs.
-- -}
-- monthField : id -> Field id
-- monthField id =
--     charField id |> fieldType Month
-- {-| A field for week inputs.
-- -}
-- weekField : id -> Field id
-- weekField id =
--     charField id |> fieldType Week
-- {-| A field for time inputs.
-- -}
-- timeField : id -> Field id
-- timeField id =
--     charField id |> fieldType Time
-- {-| A field for datetime inputs.
-- -}
-- datetimeField : id -> Field id
-- datetimeField id =
--     charField id |> fieldType Datetime
-- {-| A field for color inputs.
-- -}
-- colorField : id -> Field id
-- colorField id =
--     charField id |> fieldType Color
--- FIELD MODIFIERS ---


{-| Sets form field help text
-}
helpText : String -> Field id -> Field id
helpText text field =
    { field | helpText = Just text }


{-| Marks form field as required
-}
required : Bool -> Field id -> Field id
required required field =
    { field | required = required }


{-| Sets the placeholder string
-}
placeholder : String -> Field id -> Field id
placeholder text field =
    { field | placeholder = Just text }


{-| Sets the default value
-}
default : String -> Field id -> Field id
default text field =
    { field | default = Just text }


{-| Sets the field label
-}
label : String -> Field id -> Field id
label text field =
    { field | label = text }


{-| Adds a new validator to field
-}
validator : Validator -> Field id -> Field id
validator validator field =
    { field | validators = field.validators ++ [ validator ] }



--- MODIFIERS ---


{-| Sets the value attribute of a field
-}
setValue : String -> Field id -> Field id
setValue value state =
    { state | value = value }


{-| Adds a new error to the list of errors
-}
addError : String -> Field id -> Field id
addError error state =
    addErrors [ error ] state


{-| Appends a list of errors to the current state
-}
addErrors : List String -> Field id -> Field id
addErrors errors state =
    case errors of
        [] ->
            state

        _ ->
            let
                errors_ =
                    case state.errors of
                        Valid ->
                            Errors errors

                        Errors lst ->
                            Errors (errors ++ lst)
            in
            { state | errors = errors_ }


{-| Remove all error messages from state
-}
resetErrors : Field id -> Field id
resetErrors state =
    { state | errors = Valid }



--- VALUE READERS ---


{-| Return the field content as a string
-}
read : Field id -> String
read { value } =
    value


{-| Return field content as a boolean result.

The field must be stored internally as the "true", "false" or "" strings.
-}
readBool : Field id -> Result String Bool
readBool { value } =
    case value of
        "true" ->
            Ok True

        "false" ->
            Ok False

        _ ->
            Err "invalid boolean value"


{-| Return field state contents as a float result.
-}
readFloat : Field id -> Result String Float
readFloat { value } =
    String.toFloat value



--- UPDATE ---


{-| Updates field from message
-}
update : FormMsg id -> Field id -> Field id
update msg field =
    case msg of
        UpdateField id value ->
            if id == field.id then
                setValue value field
            else
                field

        RequestValidation id ->
            if id == field.id then
                validate field
            else
                field

        _ ->
            field


{-| Triggers field validation and return validated version
of the field.
-}
validate : Field id -> Field id
validate field =
    let
        errors =
            validateBatch field.validators field.value
    in
    { field | errors = errors }



--- VIEW FUNCTIONS ---


{-| Renders field from config and state
-}
view : Field id -> Html (FormMsg id)
view field =
    let
        input =
            viewInput field

        errors =
            case field.errors of
                Valid ->
                    []

                Errors errors ->
                    [ viewErrors [] errors ]

        children =
            (text field.label :: errors ++ [ input ])
                |> fwrapAppend (\x -> p [] [ text x ]) field.helpText
    in
    Html.label [ class "form-field" ] children


viewInput : Field id -> Html (FormMsg id)
viewInput ({ which, id } as field) =
    let
        value =
            if String.isEmpty field.value then
                field.default
            else
                Just field.value

        attrs =
            [ onInput (UpdateField id) ]
                |> fwrapAppend Attrs.placeholder field.placeholder
                |> fwrapAppend Attrs.value value
    in
    case which of
        TextArea ->
            textarea attrs []

        _ ->
            input ([ type_ <| toTypeString which ] ++ attrs) []


viewErrors : List (Attribute msg) -> List String -> Html msg
viewErrors attrs errors =
    let
        viewError x =
            li [] [ text x ]

        attrs_ =
            attrs ++ [ class "error" ]
    in
    ul attrs_ <| List.map viewError errors


