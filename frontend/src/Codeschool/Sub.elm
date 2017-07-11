module Codeschool.Sub exposing (subscriptions)

import Codeschool.Msg exposing (Msg)
import Codeschool.Model exposing (Model)


subscriptions : Model -> Sub Msg
subscriptions model =
    Sub.none
