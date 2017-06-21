module Codeschool.User
    exposing
        ( Profile
        , User
        , empty
        , fake
        )

{-| User and profiles


# Models

@docs User, Profile


# Constructors

@docs empty, fake

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


{-| A fake user that can be useful in testing.
-}
fake : User
fake =
    { name = "Albert Einstein"
    , email = "emc2@hotmail.com"
    , username = "aeinstein"
    , profile =
        { url = Just "https://eistein.blogspot.com/"
        }
    }
