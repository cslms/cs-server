module Codeschool.Dialog exposing (showDialog, showFeedbackDialog)

{-| Codeschool dialogs


# Views

@docs showDialog, showFeedbackDialog

-}

import Html exposing (..)
import Html.Attribute exposing (..)
import Dialog


showDialog : String -> String -> Html msg
showDialog title msgText =
    Dialog.render
        { styles = [ ( "class", "cs-dialog" ) ]
        , title = title
        , content = [ p [] [ text msgText ] ]
        , actionBar =
            [ button [ class "mdl-button", onClick CloseModal ] [ text "Close" ]
            ]
        }
        Dialog.visible


showFeedbackDialog : Feedback -> Html msg
showFeedbackDialog feedback =
    case feedback of
        Error msg ->
            showDialog "Error" msg

        Waiting ->
            showDialog "Waiting..." "Please wait while codeschool grade your submission"

        _ ->
            showDialog "" ""
