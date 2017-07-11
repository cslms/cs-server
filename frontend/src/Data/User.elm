module Data.User exposing (..)

{-| Represents user objects in Elm
-}

import Json.Decode as Dec exposing (..)
import Json.Encode as Enc


{-| Represents a simple user
-}
type alias User =
    { name : String
    , alias_ : String
    , email : String
    , id : Int
    }


testUser : User
testUser =
    { name = "Anonymous", alias_ = "unknown", email = "none@gmail.com", id = 1 }


{-| A decoder for user objects
-}
userDecoder : Dec.Decoder User
userDecoder =
    Dec.map4 User
        (field "name" string)
        (field "alias" string)
        (field "email" string)
        (field "id" int)


{-| Convert user to JSON
-}
toJson : User -> Dec.Value
toJson user =
    let
        str =
            Enc.string
    in
    Enc.object
        [ ( "name", str user.name )
        , ( "alias", str user.alias_ )
        , ( "email", str user.email )
        , ( "id", Enc.int user.id )
        ]


{-| Return the REST URL associated with the user
-}
toURL : User -> String
toURL user =
    "/users/" ++ toString user.id
