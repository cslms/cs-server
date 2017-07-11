module Codeschool.Model
    exposing
        ( Model
        , Route(..)
        , init
        )

{-| Page model components.
-}

import Data.User exposing (..)
import Data.Classroom exposing (Classroom, ClassroomInfo)

{-| Main page Model
-}
type alias Model =
    { user : User
    , route : Route
    , classroomInfoList : List ClassroomInfo
    , classroom : Maybe Classroom
    , loadedAssets : List String 
    }


{-| Starts the main model to default state.
-}
init : Model
init =
    { user = testUser
    , route = Index
    , classroomInfoList = []
    , classroom = Nothing 
    , loadedAssets = []
    }



---- ROUTES ----


type alias Slug =
    String


type alias Id =
    Int


{-| A list of all valid routes in Codeschool
-}
type Route
    = Index
    | NotFound
    | ClassroomList
    | Classroom Slug
    | SubmissionList
    | ScoreBoard
    | Progress
    | Learn
    | Help
    | QuestionList
    | Question Id
    | Social
    | Profile Id
    | Logout
