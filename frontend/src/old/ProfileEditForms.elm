module Codeschool.Auth.ProfileEditForms
    exposing
        ( AccountsForm
        , AccountsFormMsg
        , AccountsFormState
        , accountsForm
        )

{-| Forms for the edit profile page
-}

import Forms.Fields exposing (..)
import Forms.Form exposing (..)


type AccountsFormFields
    = Twitter
    | Github
    | Facebook
    | Google


type AccountsFormState
    = FormState AccountsFormFields


{-| Set-up the accounts form.
-}
accountsForm =
    Form.form []
        [ charField Twitter
            |> label "Twitter"
        , charField Github
            |> label "Github"
        , charField Facebook
            |> label "Facebook"
        , charField Gmail
            |> label "Google+"
            |> helpText "Your gmail e-mail"
        ]


accountsFormInit : AccountsFormState
accountsFormInit =
    formInit accountsForm


accountsFormView : FormState -> Html msg
accountsFormView state =
    view accountsForm state
