module Forms.Form
    exposing
        ( action
        , form
        , hasErrors
        , setValues
        , updateForm
        , viewForm
        )

{-| Utilities to interact with Django forms.

This module have a Python side that deals with serializing forms and exposing with a REST API.
The Elm part consume those APIs and displays forms along with content.


# Declaring a form

@docs form


## Global form options

@docs action


## Form values

@docs hasErrors


## Field properties

@docs setValues


# Messages

@docs updateForm


# View functions

@docs viewForm

-}

import Forms.Fields as Fields exposing (..)
import Forms.Types exposing (..)
import Forms.Utils exposing (..)
import Forms.Validation exposing (Validation(..))
import Html exposing (..)
import Html.Attributes as Attrs
import Html.Events exposing (..)
import Maybe


---  CONSTRUCTORS ---


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



--- MESSAGES ---


{-| Update form state from messages
-}
updateForm : FormMsg id -> Form id -> Form id
updateForm msg_ state =
    case msg_ of
        UpdateField id data ->
            let
                forEach : List a -> (a -> a) -> List a
                forEach lst func =
                    List.map func lst

                fields =
                    forEach state.fields
                        (\x ->
                            if x.id == id then
                                setValue data x
                            else
                                x
                        )
            in
            { state | fields = fields }

        SubmitForm state ->
            let
                fields =
                    List.map validateField state.fields
            in
            { state | fields = fields }

        RequestValidation id ->
            let
                fields =
                    List.map (updateField msg_) state.fields
            in
            { state | fields = fields }

        RequestFullValidation ->
            let
                fields =
                    List.map validateField state.fields
            in
            { state | fields = fields }



--- VIEW FUNCTIONS ---


{-| Renders form object
-}
viewForm : Form id -> Html (FormMsg id)
viewForm model =
    let
        attrs =
            [ onSubmit <| SubmitForm model ]
                |> fwrapAppend Attrs.action model.action

        button =
            input [ Attrs.type_ "submit" ] []

        fields =
            List.map viewField model.fields
                ++ [ button ]
    in
    Html.form attrs fields
