module Forms.Form
    exposing
        ( Form
        , FormMsg
        , action
        , form
        , hasErrors
        , setValues
        , update
        , view
        )

{-| Utilities to interact with Django forms.

This module have a Python side that deals with serializing forms and exposing with a REST API.
The Elm part consume those APIs and displays forms along with content.


# Types

@docs Form, FormMsg


# Declaring a form

@docs form


## Global form options

@docs action


## Form values

@docs hasErrors


## Field properties setters

@docs setValues


# The Elm Architecture

@docs update, view

-}

import Forms.Field as Field exposing (..)
import Forms.Util exposing (..)
import Forms.Validation exposing (Validation(..))
import Html exposing (..)
import Html.Attributes as Attrs
import Html.Events exposing (..)
import Maybe


-------------------------------------------------------------------------------
---                                TYPES                                    ---
-------------------------------------------------------------------------------


{-| Encapsulates the configuration of a form.
-}
type alias Form id =
    { action : Maybe String
    , fields : List (Field id)
    }


{-| Declares a form configuration
-}
form : List (Form id -> Form id) -> List (Field id) -> Form id
form opts fields =
    let
        applyAll opts x =
            case opts of
                [] ->
                    x

                opt :: tail ->
                    opt <| applyAll tail x
    in
    applyAll opts { action = Nothing, fields = fields }



--- VALUE GETTERS ---


{-| Return True if list has any errors
-}
hasErrors : Form id -> Bool
hasErrors f =
    not <| List.all (\x -> x.errors == Valid) f.fields



--- VALUE SETTERS ---


{-| Sets the "action" field of a FormModel.

Action is the url used to wrap

-}
action : String -> Form id -> Form id
action url form =
    { form | action = Just url }


{-| Creates a new state initialized with the given list of strings.
-}
setValues : List String -> Form id -> Form id
setValues data model =
    { model | fields = List.map2 setValue data model.fields }



-------------------------------------------------------------------------------
---                       THE ELM ARCHITECTURE                              ---
-------------------------------------------------------------------------------
--- MESSAGES ---


{-| Message type for form events.

It controls field update and validation.

-}
type FormMsg id
    = FieldMsg (FieldMsg id)
    | RequestFullValidation


{-| Update form state from messages
-}
update : FormMsg id -> Form id -> Form id
update msg_ state =
    case msg_ of
        FieldMsg msg ->
            -- Field messages
            case msg of
                UpdateField id data ->
                    let
                        fields =
                            state.fields |> List.map setThis

                        setThis x =
                            if x.id == id then
                                setValue data x
                            else
                                x
                    in
                    { state | fields = fields }

                RequestValidation id ->
                    let
                        fields =
                            List.map (Field.update msg) state.fields
                    in
                    { state | fields = fields }

        -- Global messages
        -- SubmitForm state ->
        --     let
        --         fields =
        --             List.map Field.validate state.fields
        --     in
        --     { state | fields = fields }
        RequestFullValidation ->
            let
                fields =
                    List.map Field.validate state.fields
            in
            { state | fields = fields }



--- VIEW FUNCTIONS ---


{-| Renders form object
-}
view : Form id -> Html (FormMsg id)
view model =
    let
        attrs =
            [ onSubmit RequestFullValidation ]
                |> fwrapAppend Attrs.action model.action

        button =
            input [ Attrs.type_ "submit" ] []

        fields =
            (List.map Field.view model.fields
                ++ [ button ]
            )
                |> List.map (Html.map FieldMsg)
    in
    Html.form attrs fields
