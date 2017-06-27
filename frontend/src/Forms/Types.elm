module Forms.Types
    exposing
        ( Field
        , FieldType(..)
        , Form
        , FormMsg(..)
        , JsonField
        , JsonForm
        , stringToType
        , typeToString
        )

{-| Centralize and expose all types defined for the Forms module.


# Messages

@docs FormMsg


# Config types

@docs FormConfig, FieldConfig, which


# State types

@docs FormState, Value, JsonForm, JsonField

-}

import Dict
import Forms.Validation exposing (Validation, Validator)


--- DATA TYPES (MODELS) ---


{-| Encapsulates the configuration of a form.
-}
type alias Form id =
    { action : Maybe String
    , fields : List (Field id)
    }


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



--- MESSAGES ---


{-| Field message
-}
type FormMsg id
    = UpdateField id String
    | SubmitForm (Form id)
    | RequestValidation id
    | RequestFullValidation


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
