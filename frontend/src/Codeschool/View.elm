module Codeschool.View exposing (..)

--import Html.Attributes exposing (..)

import Codeschool.Model exposing (..)
import Codeschool.Msg exposing (Msg)
import Html exposing (..)
import Page.Classroom exposing (webDetail)
import Page.Help
import Page.Index
import Page.Learn
import Page.NotFound
import Page.Profile
import Page.Progress
import Page.Questions.Base
import Page.ScoreBoard
import Page.Social
import Page.Submission
import Ui.Layout


view : Html Msg -> Model -> Html Msg
view x m =
    let
        data =
            case m.route of
                ClassroomList ->
                    Page.Classroom.classroomList Page.Classroom.clsList

                Classroom id ->
                    Page.Classroom.classroomList Page.Classroom.clsList

                Help ->
                    Page.Help.view m

                Index ->
                    Page.Index.view m

                Learn ->
                    Page.Learn.view m

                Logout ->
                    Page.Index.view m

                Profile id ->
                    Page.Profile.view m

                Progress ->
                    Page.Progress.view m

                QuestionList ->
                    Page.Questions.Base.viewList m

                Question id ->
                    Page.Questions.Base.viewDetail m

                ScoreBoard ->
                    Page.ScoreBoard.view m

                Social ->
                    Page.Social.view m

                SubmissionList ->
                    Page.Submission.view m

                NotFound ->
                    Page.NotFound.view m
    in
    Ui.Layout.page data m
