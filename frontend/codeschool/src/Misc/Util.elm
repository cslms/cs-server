module Misc.Util exposing (closestDate)

{-| Misc utility functions. Implements a few random bits missing in Elm's
standard library
-}

import Date exposing (Date, Month)


{-| Return the closest valid date to the given tuple of (year, month, day)
-}
closestDate : ( Int, Int, Int ) -> Date
closestDate ( year, month, day ) =
    let
        stDate =
            toString year ++ "/" ++ toString month ++ "/" ++ toString day
    in
    case Date.fromString stDate of
        Ok x ->
            x

        Err _ ->
            epochDateFallback


{-| TODO: remove this hack and implement closestDate correctly!
-}
epochDateFallback : Date
epochDateFallback =
    Date.fromTime 0.0
