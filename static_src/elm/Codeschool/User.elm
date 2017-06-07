module Codeschool.User
    exposing
        ( Profile
        , User
        , empty
        )

{-| User and profiles


# Models

@docs User, Profile


# Constructors

@docs empty

-}


-- MODELS


{-| Base user model. Can be accessed via /api/users/{id}/
-}
type alias User =
    { name : String
    , email : String
    , username : String
    , profile : Profile
    }


{-| Profile for user. Accessed at /api/users/{id}/profile
-}
type alias Profile =
    { url : Maybe String
    }


{-| Creates an empty user
-}
empty : User
empty =
    { name = "?", email = "", username = "?", profile = { url = Nothing } }
