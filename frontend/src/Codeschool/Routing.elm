module Codeschool.Routing exposing (parseLocation, reverse)

import Codeschool.Model exposing (Route(..))
import Navigation exposing (Location)
import UrlParser exposing (..)


matchers : Parser (Route -> a) a
matchers =
    oneOf
        [ map Index top
        , map Classroom (s "classrooms" </> string)
        , map ClassroomList (s "classrooms/")
        , map SubmissionList (s "submissions")
        , map ScoreBoard (s "score")
        , map Progress (s "progress")
        , map Learn (s "learn")
        , map Help (s "help")
        , map Question (s "questions" </> int)
        , map QuestionList (s "questions")
        , map Social (s "social")
        , map Profile (s "profile" </> int)
        , map Logout (s "logout")
        ]


{-| Convert location to route
-}
parseLocation : Location -> Route
parseLocation location =
    case parseHash matchers location of
        Just route ->
            route

        Nothing ->
            NotFound


{-| Reverse URL without using the # prefix.
-}
baseReverse : Route -> String
baseReverse route =
    case route of
        Index ->
            ""

        Classroom st ->
            "classrooms/" ++ st

        ClassroomList ->
            "classrooms/"

        SubmissionList ->
            "submissions/"

        ScoreBoard ->
            "score/"

        Progress ->
            "progress/"

        Learn ->
            "learn/"

        Help ->
            "help/"

        Question id ->
            "questions/" ++ toString id

        QuestionList ->
            "questions/"

        Social ->
            "social"

        Profile id ->
            "profile/" ++ toString id

        Logout ->
            "logout/"

        NotFound ->
            "404.html"


{-| Reverse URL prepending the "#" symbol
-}
reverse : Route -> String
reverse route =
    "#" ++ baseReverse route
