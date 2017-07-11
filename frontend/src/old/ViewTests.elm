module ViewTests exposing (..)

import Html exposing (..)
import Html.Attributes exposing (..)
import Html.Keyed as Key
import Page.Model exposing (Model)


view : model -> Html msg
view m =
    div []
        [ h1 [] [ text "Keyed elements" ]
        , div []
            [ Key.node "foo"
                []
                [ -- materialize
                  ( "materialize"
                  , button [ class "waves-effect waves-light btn" ]
                        [ text "Materialize"
                        ]
                  )

                -- web components
                , ( "mcw"
                  , button
                        [ class "mdc-button mdc-button--raised"
                        , attribute "data-mdc-auto-init" "MDCRipple"
                        ]
                        [ text "MDC for Web"
                        ]
                  )

                -- mdl
                , ( "mdl"
                  , button [ class "mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect" ]
                        [ text "MDL.io" ]
                  )
                ]
            ]
        , h1 [] [ text "Non-keyed elements " ]
        , div []
            [ -- materialize
              button [ class "waves-effect waves-light btn" ]
                [ text "Materialize"
                ]

            -- mcw
            , button
                [ class "mdc-button mdc-button--raised"
                , attribute "data-mdc-auto-init" "MDCRipple"
                ]
                [ text "MDC for Web"
                ]

            -- mdl
            , button [ class "mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect" ]
                [ text "MDL.io" ]
            ]

        -- vue
        , div [ id "vue-elm" ]
            [ node "md-toolbar"
                []
                [ h1 [ class "md-title" ] [ text "Vue test" ]
                ]
            ]

        -- Polymer
        , h1 [] [ text "polymer" ]
        , div []
            [ node "paper-button"
                [ class "pink" ]
                [ text "link" ]
            , node "paper-button"
                [ raised, class "indigo" ]
                [ text "raised" ]
            , node "paper-button"
                [ toggles, raised, class "green" ]
                [ text "toggles" ]
            , node "paper-button"
                [ disabled, class "disabled" ]
                [ text "disabled" ]
            ]

        -- X-tag
        , h1 [] [ text "x-tag" ]
        , node "x-clock" [] []
        ]


raised =
    attribute "raised" "raised"


toggles =
    attribute "toggles" "toggles"


disabled =
    attribute "disabled" "disabled"
