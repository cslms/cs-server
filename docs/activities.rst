=======================================
Activities/Progress/Submission/Feedback
=======================================

Many students interactions with Codeschool is done through the activities/
progress/submission/get_feedback cycle. Let us explain exactly the role of each
part and how students interactions are processed.

Activities:
    Define a task or any other activity that the student should respond to.
    Activities can be complex things such as "make this huge programming
    project" or very simple things such as the task "download this file".

    Many important things in codeschool are implemented as Activities:
    questions, quizzes, #TO-DO, etc.

Progress:
    Once the student access an activity, Codeschool starts tracking its
    progress. This creates an object that keeps track of all submissions and
    the student performance. There is a unique Progress object per student per
    Activity. It is responsible for awarding points and of increasing the total
    student XP.

Submission:
    Each interaction with an activity produces a submission.

Feedback:
    Submissions and Progress objects can be judged and produce a Feedback.
