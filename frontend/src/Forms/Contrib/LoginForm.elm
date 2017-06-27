module Forms.Contrib.LoginForm
    exposing
        ( LoginFields(..)
        , LoginForm
        , LoginFormMsg
        , LoginFormTypes
        , login
        , loginByEmail
        , loginByUsername
        )

{-| Some reusable form components


# Login

@docs LoginFields, login

-}

import Forms.Fields exposing (..)
import Forms.Form as Form exposing (..)
import Forms.Types exposing (..)


type LoginFields
    = Username
    | Password
    | Submit


type LoginFormTypes
    = ByUsername
    | ByEmail


type alias LoginForm =
    Form LoginFields


type alias LoginFormMsg =
    FormMsg LoginFields


{-| A login form component that may use e-mail or username
-}
login : LoginFormTypes -> LoginForm
login which =
    let
        ( userField, userLabel ) =
            case which of
                ByEmail ->
                    ( emailField, "E-mail" )

                ByUsername ->
                    ( charField, "Username" )
    in
    Form.form []
        [ userField Username
            |> label userLabel
            |> placeholder ("Enter your " ++ String.toLower userLabel)
        , passwordField Password
            |> label "Password"
            |> placeholder "Enter your password"
        ]


loginByEmail : LoginForm
loginByEmail =
    login ByEmail


loginByUsername : LoginForm
loginByUsername =
    login ByUsername
