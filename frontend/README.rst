=========================
Codeschool frontend stack
=========================


Codechool uses Django + Django Rest Framework on the backend and comunicates with a Elm-based frontend
via API. This file describes the basic technologies and archtechiture for the frontend part.



Installing
==========

The first step is to install the Javascript dependencies and Elm in your system. We offer an invoke script
to install everything in a single shot:

    $ inv install-frontend

If that command does not work, you have to enable the manual override :)


**Global dependencies**

Many Javascript dependencies must be installed globally (most notably Elm and webpack).
Let us start with them first. 

    $ sudo apt-get install nodejs ruby
    $ sudo npm install -g webpack elm-language create-elm-app

(the last time we tried, this command did not work with yarn).
    
Secondly, we need to install the elm-install package

    $ sudo apt-get install yarn
    $ gem install elm_install
    $ npm install elm-github-install -g

(Now you have to replace npm by yarn, what a mess!).


**Local dependencies**

The next step is to build the local node_modules folder for your project. This part can
use `npm` or `yarn`. 

    $ cd frontend
    $ npm install  

Wait a few minutes while it installs all dependencies.


**Docker dev image**

Someday we will also provide a docker image for development.



Tech stack
==========

Elm
---

Frontend is written mostly in Elm, which is a functional Haskell-like language for the web. 
uses an archtechiture which is now getting popular in the Javascript world. It has inspired React + Flux and  
Vue + Vuex.


Material Design
---------------


Ace.js
------


Messing around
==============

Now you want to tweak the codeschool interface? 