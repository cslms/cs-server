module Data.Classroom exposing (..)

{-| Classroom representations
-}

import Date exposing (Date)
import Json.Decode as Dec exposing (..)
import Json.Encode as Enc


{-| Represents the reduced information about a classroom that is shown on listings
-}
type alias ClassroomInfo =
    { name : String
    , teacher : String
    , shortDescription : String
    }


{-| Full info on a classroom
-}
type alias Classroom =
    { name : String
    , teacher : String
    , shortDescription : String
    , longDescription : String
    , lessons : List Lesson
    }


{-| Full info on a classroom
-}
type alias Lesson =
    { date : Date
    , description : String
    }



---- JSON ENCODE/DECODE ----


classroomInfoDecoder : Decoder ClassroomInfo
classroomInfoDecoder =
    Dec.map3 ClassroomInfo
        (field "name" string)
        (field "teacher" string)
        (field "short_description" string)


classroomDecoder : Decoder Classroom
classroomDecoder =
    Dec.map5 Classroom
        (field "name" string)
        (field "teacher" string)
        (field "short_description" string)
        (field "long_description" string)
        (field "lessons" (list lessonDecoder))


lessonDecoder : Decoder Lesson
lessonDecoder =
    Dec.map2 Lesson
        (field "date" dateDecoder)
        (field "description" string)


dateDecoder : Decoder Date
dateDecoder =
    let
        conv x =
            case Date.fromString x of
                Ok st ->
                    succeed st

                Err msg ->
                    fail msg
    in
    string |> andThen conv


toJson : Classroom -> Enc.Value
toJson cls =
    let
        str =
            Enc.string
    in
    Enc.object
        [ ( "name", str cls.name )
        , ( "teacher", str cls.teacher )
        , ( "shortDescription", str cls.shortDescription )
        ]

