module Dialog exposing (Config, Visible, visible, hidden, render)

{-| Elm Mdl Dialog

@docs Config, render, Visible, hidden, visible
-}

import Html exposing (..)
import Html.Attributes exposing (..)


{-| The Dialog Configuration.

`styles` sets inline styles for the dialog div. You may e.g. want to set a width.
`title` sets a header title. Since MDL does the styling, you only need to provide
a string.
`content` is where you put all your Html to be displayed in the Dialog's body.
`actionBar` sits at bottom of the Dialog. You may want to place some actions there,
usually at least one close button.

-}
type alias Config msg =
    { styles : List ( String, String )
    , title : String
    , content : List (Html msg)
    , actionBar : List (Html msg)
    }


{-| A helper to make things more humand readable. Use it like this:

    type alias Model =
        { myDialogVisible : Visible
        }

In the init function initialize it like this:

    init =
        { myDialogVisible = Dialog.hidden
        }

-}
type alias Visible =
    Bool


{-| A helper function that returns False to make things more human readable
-}
hidden : Visible
hidden =
    False


{-| A helper function that returns True to make things more human readable
-}
visible : Visible
visible =
    True


{-| Render the Dialog

    Dialog.render
        { styles = [ ("width", "40%") ]
        , title = "My Dialog"
        , content = [ text "This is my dialog's body." ]
        , actionBar = [ button [ onClick ToggleMyDialogVisible ] [ text "Close" ] ] }
        model.myDialogVisible

You take care of the open and close Msg yourself. Just include a Visible in your
model for each Dialog.

    type alias Model =
        { myDialogVisible : Visible
        }

    update msg model =
        case msg of
            ToggleMyDialogVisible ->
                { model | myDialogVisible = not model.myDialogVisible } ! []

-}
render : Config msg -> Visible -> Html msg
render config visible =
    let
        visibility =
            if visible == True then
                (,) "display" "flex"
            else
                (,) "display" "none"

        dialogStyle =
            dialogBaseStyle ++ config.styles
    in
        div [ style <| overlayStyle ++ [ visibility ] ]
            [ div [ style dialogStyle ]
                [ div [ class "mdl-dialog__title" ] [ text config.title ]
                , div [ class "mdl-dialog__content" ] config.content
                , div [ class "mdl-dialog__actions" ] config.actionBar
                ]
            ]


overlayStyle : List ( String, String )
overlayStyle =
    [ (,) "position" "fixed"
    , (,) "overflow-x" "hidden"
    , (,) "top" "0"
    , (,) "left" "0"
    , (,) "bottom" "0"
    , (,) "right" "0"
    , (,) "z-index" "10"
    , (,) "background-color" "rgba(0,0,0,0.5)"
    , (,) "justify-content" "center"
    , (,) "align-items" "center"
    ]


dialogBaseStyle : List ( String, String )
dialogBaseStyle =
    [ (,) "min-width" "300px"
    , (,) "background-color" "white"
    , (,) "padding" "8px 16px 8px 16px"
    , (,) "border-radius" "4px"
    , (,) "border" "1px solid #757575"
    , (,) "box-shadow" "4px 4px 5px 0px rgba(97,97,97,1)"
    ]
