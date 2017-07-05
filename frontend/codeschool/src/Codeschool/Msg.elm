module Codeschool.Msg exposing (..)

{-| Main page messages and update function
-}

import Codeschool.Model exposing (Model, Route)
import Navigation exposing (Location)
import Routing exposing (parseLocation)


{-| Message type
-}
type Msg
    = OnLocationChange Location
    | OnRouteChange Route
    | RequireAsset String
    | AssetLoaded String


{-| Update function
-}
update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        OnLocationChange loc ->
            update (OnRouteChange (parseLocation loc)) model

        OnRouteChange route ->
            { model | route = route } ! []

        RequireAsset asset ->
            if List.any ((==) asset) model.loadedAssets then
                model ! [] --- TODO: send a message requesting to load an asset 
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
