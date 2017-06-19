module Main exposing (..)

import Codeschool.Navbar as Navbar exposing (..)
import Codeschool.Page as Page exposing (contentHeader)
import Codeschool.User as User exposing (User)
import Codeschool.Wagtail as Wagtail exposing (StreamField)
import Html exposing (..)
import Html.Attributes exposing (..)
import Html.Events exposing (..)
import Maybe
import String


-- MODEL


type alias Model =
    { user : User
    , showEnrolledClassrooms : Bool
    , classrooms :
        { enrolled : List Classroom
        , other : List Classroom
        }
    }


model : Model
model =
    { user = User.fake
    , showEnrolledClassrooms = True
    , classrooms =
        { enrolled = []
        , other = []
        }
    }


modelFake : Model
modelFake =
    let
        cls =
            model.classrooms
    in
    { model | classrooms = { cls | enrolled = [ classroomFake ] } }


{-| Represents a classroom state
-}
type alias Classroom =
    { name : String
    , slug : String
    , shortDescription : String
    , longDescription : StreamField
    , teacher : User
    , students : List User
    , staff : List User
    , weeklyLessons : Bool
    , acceptSubscriptions : Bool
    }


{-| Creates an empty classroom
-}
classroom : Classroom
classroom =
    { name = ""
    , slug = ""
    , shortDescription = ""
    , longDescription = []
    , teacher = User.empty
    , students = []
    , staff = []
    , weeklyLessons = False
    , acceptSubscriptions = True
    }


classroomFake : Classroom
classroomFake =
    { classroom | name = "Elm", slug = "elm", shortDescription = "A course on the Elm language" }



-- ACTION, UPDATE


type Msg
    = SelectClassroom Int
    | SelectEnrolledClassroomsList Bool


update : Msg -> Model -> Model
update msg model =
    case msg of
        SelectEnrolledClassroomsList enrolled ->
            { model | showEnrolledClassrooms = enrolled }

        _ ->
            model



-- VIEW


view : Model -> Html Msg
view ({ classrooms, user } as model) =
    let
        head_ =
            [ Page.header
            , div
                [ id "cs-body"
                , class "mdl-grid mdl-grid mdl-grid--no-spacing"
                , style [ ( "width", "100%" ) ]
                ]
                [ div [ id "content-area", class "cs-stripes-layout" ]
                    [ main_ model ]
                ]
            ]
    in
    div [ class "cs-base-page", attribute "unresolved" "unresolved" ]
        (head_ ++ [ Page.footer ])


main_ : Model -> Html Msg
main_ model =
    Html.main_ [ class "cs-stripes-layout__main" ]
        [ div [ class "cs-stripes-layout__content" ]
            [ contentHeader "List of courses" "This lists shows all courses available to you in the codeschool application"
            , div [] [ mainTabs model ]
            ]
        ]


{-| Render tabs with course lists
-}
mainTabs : Model -> Html Msg
mainTabs model =
    let
        selectedTab =
            if model.showEnrolledClassrooms then
                renderEnrolledCourses model.classrooms.enrolled
            else
                renderOtherCourses model.classrooms.other
    in
    div [ class "mdl-tabs mdl-js-tabs mdl-js-ripple-effect" ]
        [ div [ class "mdl-tabs__tab-bar" ]
            [ a [ class "mdl-tabs__tab is-active", onClick (SelectEnrolledClassroomsList True) ]
                [ text "Enrolled" ]
            , a [ class "mdl-tabs__tab", onClick (SelectEnrolledClassroomsList False) ]
                [ text "Other" ]
            ]
        , selectedTab
        ]


renderClassromList : String -> List Classroom -> Html msg
renderClassromList err classrooms =
    if List.isEmpty classrooms then
        div [ class "mdl-tabs__panel" ]
            [ div [] [ text err ]
            ]
    else
        ul [ class "cs-course-list" ] <|
            List.map (\x -> li [] [ renderClassromItem x ]) <|
                classrooms


renderEnrolledCourses : List Classroom -> Html msg
renderEnrolledCourses classrooms =
    renderClassromList "You are not enrolled in any courses!" classrooms


renderOtherCourses : List Classroom -> Html msg
renderOtherCourses classrooms =
    renderClassromList "No courses available!" classrooms


renderClassromItem : Classroom -> Html msg
renderClassromItem classroom =
    div [ class "cs-course-list__item mdl-shadow--4dp" ]
        [ h1 [] [ text classroom.name ]
        ]


main : Program Never Model Msg
main =
    Html.beginnerProgram
        { model = modelFake
        , view = view
        , update = update
        }
