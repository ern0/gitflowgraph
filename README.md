# GitFlowGraph

Creates pretty graph from a GitFlow compliant GIT repository

## Why

This is how GitFlow looks in educational materials:

![GitFlow Educational Figure](http://nvie.com/img/git-model@2x.png "GitFlow")
*(image source: http://nvie.com/posts/a-successful-git-branching-model/)*

And this is how it looks in the real life:

![GitFlow Generated Figure](http://endoflineblog.com/assets/gitflow-mess-cfd9aa7a4137e3e575510fcbbf38a5b6.png "GitFlow")
*(image source: http://endoflineblog.com/gitflow-considered-harmful)*

I've tried some GIT clients, but even ones wich has GitFlow support render messy tree.

But I want to see GIT repositories similar way I've seen in examples.

## How

When the user launches the python backend program, it checks whether the CLI argument specified is a valid GIT repository or not. Upon success, it starts a tiny web server, and prints a link where it can be accessed. The web client downloads a JSON file from the backend web server, which contains a tree definition with all information required to display a pretty tree.

The backend is written in Python, and uses GitPython library for parsing GIT repository. The frontend runs in a browser, so it is written in JavaScript.
