module App exposing (..)

import Codeschool.Model as M
import Codeschool.Tea as Tea
import Codeschool.View
import Html exposing (div, h1, text)
import Ui.Layout
import Ui.Parts exposing (promoSimple, promoTable)


---- MODEL ----

main : Program String M.Model Tea.Msg
main =
    Tea.mainWithFlags