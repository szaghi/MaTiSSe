# MaTiSSe.py usage example: a getting started tutorial

A KISS usage example of MaTiSSe.py

## Description

This example consists of a *getting started* tutorial. The tree of the example is

```bash
|-- getting_started
|-- getting_started.md
|-- images
|-- main_theme.md
|-- README.md
```
where 
+ `getting_started.md` is the source of the presentation;
+ `main_theme.md` is the theme definition used into the presentation;
+ `images` is a directory containing images resources used into the presentation;
+ `getting_started` is the directory of the compiled html presentation;
+ `READMEmd` is the file you are reading.

For testing the example type:

```bash
MaTiSSe.py -i getting_started.md --toc-at-subsec-beginning 2
```
