module Codeschool.Assets exposing (..)

{-| Server-side assets. Controls where information is obtained on the server.
-}


type alias Id =
    Int


type Asset
    = User Id
    | UserList


{-| Return Url for the given asset
-}
url : Asset -> String
url asset =
    case asset of
        User id ->
            "/api/users/" ++ toString id

        UserList ->
            "/api/users/"
