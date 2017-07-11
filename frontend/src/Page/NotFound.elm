module Page.NotFound exposing (view)

-- import Codeschool.Msg exposing (..)
-- import Data.User exposing (User)

import Codeschool.Model exposing (Model)
import Html exposing (..)


-- import Html.Attributes exposing (..)
-- import Html.Events exposing (..)


view : Model -> Html msg
view m =
    div [] [ text "Not Found!" ]
