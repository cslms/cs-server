module Forms.Util
    exposing
        ( (::?)
        , (|>?)
        , fwrap
        , fwrapAppend
        , just2
        , just3
        , just4
        , wrap
        )

{-| Utility functions

@docs just2, just3, just4, fwrap, fwrapAppend, wrap, wrapAppend

-}

--- UTILITY FUNCTIONS ---


{-| Wrap maybe on a single or zero element list
-}
wrap : Maybe a -> List a
wrap x =
    case x of
        Just a ->
            [ a ]

        Nothing ->
            []


{-| Wrap maybe on a single or zero element list
-}
(::?) : List a -> Maybe a -> List a
(::?) lst x =
    lst ++ wrap x


{-| Pipe operator that respects Maybes
-}
(|>?) : Maybe a -> (a -> b) -> Maybe b
(|>?) x f =
    case x of
        Just a ->
            Just (f a)

        Nothing ->
            Nothing


{-| Append wrapped element to list if element is defined

The given function (a -> b) must wrap the input Maybe element.

Used to create elements that can be chained later with maybeApplyAppend:

    fwrap toString Just 42
        |> fwrapAppend toString Nothing

-}
fwrap : (a -> b) -> Maybe a -> List b
fwrap f x =
    case x of
        Just a ->
            [ f a ]

        Nothing ->
            []


{-| Append wrapped element to list if element is defined.

The given function (a -> b) must wrap the input Maybe element.

Used in chains:

    ["1", "2"]
        |> fwrapAppend toString Just 42

-}
fwrapAppend : (a -> b) -> Maybe a -> List b -> List b
fwrapAppend f x lst =
    lst ++ fwrap f x


{-| Return the defined element. The result can be Nothing if all elements are undefined
-}
just2 : Maybe a -> Maybe a -> Maybe a
just2 x y =
    case x of
        Just a ->
            x

        _ ->
            y


{-| Return the defined element. The result can be Nothing if all elements are undefined
-}
just3 : Maybe a -> Maybe a -> Maybe a -> Maybe a
just3 x y z =
    just2 x <| just2 y z


{-| Return the defined element. The result can be Nothing if all elements are undefined
-}
just4 : Maybe a -> Maybe a -> Maybe a -> Maybe a -> Maybe a
just4 x y z w =
    just2 x <| just3 y z w
