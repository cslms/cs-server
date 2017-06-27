module Forms.Contrib.FieldForm
    exposing
        ( FieldFields(..)
        , FieldForm
        , FieldFormMsg
        , field
        )

{-| Some reusable form components


# Field

@docs FieldFields, Field

-}

import Forms.Fields exposing (..)
import Forms.Form as Form exposing (..)
import Forms.Types exposing (..)


type FieldFields
    = Id
    | Label
    | Type
    | Default
    | HelpText
    | Placeholder


type alias FieldForm =
    Form FieldFields


type alias FieldFormMsg =
    FormMsg FieldFields


{-| A Field form component that may use e-mail or username
-}
field : FieldForm
field =
    Form.form []
        [ charField Id
            |> label "Id"
            |> helpText "Unique identification string"
        , charField Label
            |> label "Label"
            |> helpText "Label visible to the user"
        , charField Type
            |> label "Type"
            |> helpText "Input type"
        , charField Default
            |> label "Default value"
        , charField HelpText
            |> label "Help"
            |> helpText "A message explaining the usage of the field. Just like this message you are reading ;)"
        , charField Placeholder
            |> label "Placeholder"
            |> helpText "A help message displayed directly on the field."
        ]
