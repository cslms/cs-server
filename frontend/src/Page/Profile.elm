module Page.Profile exposing (view)

import Codeschool.Model exposing (Model)
import Html exposing (..)
import Ui.Generic exposing (container)
import Ui.Parts exposing (promoSimple, promoTable, simpleHero)


type alias Profile =
    { name : String, email : String }


profile =
    { name = "John Smith", email = "foo@google.com" }


view : Model -> Html msg
view m =
    div []
        [ simpleHero profile.name "Profile"
        , container []
            [ h1 [] [ text "Personal info" ]
            , p [] [ text ("Name: " ++ profile.name) ]
            , p [] [ text ("E-mao;: " ++ profile.email) ]
            ]
        ]
