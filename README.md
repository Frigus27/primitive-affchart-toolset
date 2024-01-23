# Primitive AffChart Toolset

A primitive AffChart Toolset example.

# Wait, what is AffChart?

AffChart is a project which aims to provide a tool on Python to operate on Arcaea chart file (.aff). The first version of AffChart (a.k.a. Primitive AffChart) is designed and developed in my highschool stage which, due to the busy chores and no leisure time every day, is quite simple, primitive and shabby. With Primitive AffChart I have made several tools which helps to do some chores like speeding a chart, making forward a chart for some stamps, generating songlist, etc.

And now is my college vacation, and I want to make AffChart a more technologically mature platform rather than keep it old. That is my reason to publish my scripts written before. These scripts, because of the busy time I have experienced, is written in a quick-but-dirty style and is considered no longer in maintainance. Therefore the code can work, but is not an example to follow.

# Files

## afflex.py

The core module which offers `AffFile, AffElements, AffTimingGroup` classes which are used to lex a piece of Arcaea chart. It provides a minimum level of abstraction to operate on a chart which just help you to load a file, fill in the parameters, and save a file.

## afffrwrd.py (Aff Forward)

A tool to help move the chart forward by a time stamp. The negative (or overmoved) part is not trimmed and the `scenecontrol` parameters is not moved as well as `camera`.

## affspeed.py (Aff Speed)

A tool to help speed up or slow down a chart by a given ratio to stretch bpm. The not-moved objects is as the same as `afffrwrd.py`.

## slgen.py (Songlist Generator)

A tool to help generate a songlist template for a chart. You offer a template and all charts packed in folders, and it read all aff files, get the bpm data and generate a total songlist file with the template and simple info filled.

## affsplit.py (Aff Split)

The tool helps to extract the arctaps on every traces and made them independent and not guided (i.e. guided on a trace whose time stamp period is only 1). This tool is written today and you may see new code styles in it, which is my goal to revolute the toolset.
