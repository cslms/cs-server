module Codeschool.Msg exposing (..)

{-| Main page messages and update function
-}

import Codeschool.Model exposing (Model, Route)
import Codeschool.Routing exposing (parseLocation, reverse)
import Navigation exposing (Location, newUrl)


{-| Message type
-}
type Msg
    = ChangeLocation Location
    | ChangeRoute Route
    | RequireAsset String
    | AssetLoaded String


{-| Update function
-}
update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        ChangeRoute route ->
            model ! [ newUrl (reverse route) ]

        ChangeLocation loc ->
            { model | route = parseLocation loc } ! []
        
        RequireAsset asset ->
            if List.any ((==) asset) model.loadedAssets then
                model ! []
                --- TODO: send a message requesting to load an asset
            else
                model ! []

        AssetLoaded asset ->
            { model | loadedAssets = withElement asset model.loadedAssets } ! []


{-| Return a new list that surely include the given element
-}
withElement : a -> List a -> List a
withElement el lst =
    if List.any ((==) el) lst then
        lst
    else
        el :: lst
