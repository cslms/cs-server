module Forms.Validation
    exposing
        ( Validation(..)
        , Validator(..)
        , email
        , extensions
        , fromInfo
        , maxLength
        , maxValue
        , minLength
        , minValue
        , notEmpty
        , numeric
        , regex
        , url
        , validateBatch
        , validatorInfo
        )

{-| Convert validator element to a validation function


# Validation functions

@docs validate, validateBatch

-}

import Forms.Value as Value exposing (Value(..))


--- BASIC TYPES  ---


type alias Err =
    String


type alias ValueOpt tt =
    { value : tt }


type alias ExtensionsOpt =
    { extensions : List String }


type alias DecimalOpt =
    { places : Int, size : Int }


type alias EmptyOpt =
    {}


{-| Supported validators
-}
type Validator
    = NotEmpty Err EmptyOpt
    | Numeric Err EmptyOpt
    | Email Err EmptyOpt
    | Url Err EmptyOpt
    | Decimal Err DecimalOpt
    | Extensions Err ExtensionsOpt
    | Regex Err (ValueOpt String)
    | MinLength Err (ValueOpt Int)
    | MaxLength Err (ValueOpt Int)
    | MinValue Err (ValueOpt Float)
    | MaxValue Err (ValueOpt Float)


{-| The result of a validation
-}
type Validation
    = Valid
    | Errors (List String)



--- VALIDATOR CONSTRUCTORS ---


{-| Sets the minimum value for numeric field
-}
minValue : Float -> String -> Validator
minValue x msg =
    MinValue msg (ValueOpt x)


{-| Sets the maximum value for numeric field
-}
maxValue : Float -> String -> Validator
maxValue x msg =
    MaxValue msg (ValueOpt x)


{-| Sets the minimum length for string field
-}
minLength : Int -> String -> Validator
minLength x msg =
    MinLength msg (ValueOpt x)


{-| Sets the maximum length for string field
-}
maxLength : Int -> String -> Validator
maxLength x msg =
    MaxLength msg (ValueOpt x)


{-| Forces numeric input
-}
numeric : String -> Validator
numeric msg =
    Numeric msg {}


{-| Prevents empty inputs
-}
notEmpty : String -> Validator
notEmpty msg =
    NotEmpty msg {}


{-| Checks if input is a valid email
-}
email : String -> Validator
email msg =
    Email msg {}


{-| Checks if input is a valid url
-}
url : String -> Validator
url msg =
    Email msg {}


{-| Checks if input is a valid url
-}
extensions : List String -> String -> Validator
extensions exts msg =
    Extensions msg (ExtensionsOpt exts)


{-| Uses a regular expression to validate field
-}
regex : String -> String -> Validator
regex re msg =
    Regex msg (ValueOpt re)



--- VALIDATION FUNCTIONS ---


{-| Uses a validator to validate a value.

The result is a Valid | Errors list of error messages

-}
validate : Validator -> String -> Validation
validate val x =
    let
        -- Auxiliary functions
        validateNumericOp : String -> (Float -> Float -> Bool) -> Float -> String -> Validation
        validateNumericOp x op y err =
            let
                x_num =
                    String.toFloat x
            in
            case x_num of
                Ok x ->
                    if op x y then
                        Errors [ err ]
                    else
                        Valid

                Err _ ->
                    Errors [ err ]
    in
    case val of
        NotEmpty err _ ->
            if String.isEmpty x then
                Valid
            else
                Errors [ err ]

        Numeric err _ ->
            case String.toFloat x of
                Ok _ ->
                    Valid

                Err _ ->
                    Errors [ err ]

        MinLength err { value } ->
            if String.length x < value then
                Errors [ err ]
            else
                Valid

        MaxLength err { value } ->
            if String.length x > value then
                Errors [ err ]
            else
                Valid

        MinValue err { value } ->
            validateNumericOp x (<) value err

        MaxValue err { value } ->
            validateNumericOp x (>) value err

        -- TODO: implement other validators
        _ ->
            Valid


{-| Validate value using a list of validators
-}
validateBatch : List Validator -> String -> Validation
validateBatch validators data =
    let
        results : List Validation
        results =
            List.map (\validator -> validate validator data) validators

        reducer : Validation -> Validation -> Validation
        reducer =
            \r1 r2 ->
                case ( r1, r2 ) of
                    ( Valid, Valid ) ->
                        Valid

                    ( Errors _, Valid ) ->
                        r1

                    ( Valid, Errors _ ) ->
                        r2

                    ( Errors err1, Errors err2 ) ->
                        Errors <| err1 ++ err2
    in
    List.foldr reducer Valid results



--- INTROSPECTION FUNCTIONS ---


{-| Return a string used to represent the Validator in JSON data
-}
validatorInfo : Validator -> ( String, String, List ( String, Value ) )
validatorInfo val =
    case val of
        -- Empty options
        Numeric err _ ->
            ( "numeric", err, [] )

        NotEmpty err _ ->
            ( "not-empty", err, [] )

        Email err _ ->
            ( "is-email", err, [] )

        Url err _ ->
            ( "is-url", err, [] )

        -- Single value options
        Extensions err { extensions } ->
            ( "extensions", err, [ ( "extensions", List <| List.map String extensions ) ] )

        Regex err { value } ->
            ( "regex", err, [ ( "value", String value ) ] )

        MinLength err { value } ->
            ( "min-length", err, [ ( "value", Int value ) ] )

        MaxLength err { value } ->
            ( "max-length", err, [ ( "value", Int value ) ] )

        MinValue err { value } ->
            ( "min-value", err, [ ( "value", Float value ) ] )

        MaxValue err { value } ->
            ( "max-value", err, [ ( "value", Float value ) ] )

        -- Multi-value options
        Decimal err { places, size } ->
            ( "decimal", err, [ ( "places", Int places ), ( "size", Int size ) ] )


{-| Attempt to build validator from (name, error, [options]) data.
-}
fromInfo : ( String, String, List ( String, Value ) ) -> Result String Validator
fromInfo (( name, err, opts ) as info) =
    let
        try factory opts err =
            case opts of
                Ok opt ->
                    Ok (factory opt err)

                Err _ ->
                    Err ("invalid info: " ++ toString info)

        extract : String -> (Value -> Result String a) -> List ( String, Value ) -> Result String a
        extract field conv opts =
            case single field opts of
                Just x ->
                    conv x

                Nothing ->
                    Err ""

        single : String -> List ( String, Value ) -> Maybe Value
        single field opts =
            case opts of
                ( field, v ) :: [] ->
                    Just v

                _ ->
                    Nothing

        toExtensions : Value -> Result String (List String)
        toExtensions v =
            case v of
                List xs ->
                    Ok (List.map Value.toString xs)

                _ ->
                    Err ""
    in
    case name of
        "numeric" ->
            Ok (numeric err)

        "not-empty" ->
            Ok (notEmpty err)

        "is-email" ->
            Ok (email err)

        "is-url" ->
            Ok (url err)

        "extensions" ->
            try extensions (extract "extensions" toExtensions opts) err

        "regex" ->
            try regex (extract "value" (\x -> Ok <| Value.toString x) opts) err

        "min-length" ->
            try minLength (extract "value" Value.toInt opts) err

        "max-length" ->
            try maxLength (extract "value" Value.toInt opts) err

        "min-value" ->
            try minValue (extract "value" Value.toFloat opts) err

        "max-value" ->
            try maxValue (extract "value" Value.toFloat opts) err

        _ ->
            Err ("invalid info: " ++ toString info)
