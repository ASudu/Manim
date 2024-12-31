# Manim

In this repository, I try out a few math animations as a learning experience

All the animation files can be found in `project/`

## Setup

The `ManimCE` has really good documentation for the [setup](https://docs.manim.community/en/stable/installation.html) based on your requirement

## Quickstart

- For a quick example, you can check out `project/qucikstart.py` which has 3 short examples inspired from `ManimCE` documentation.
- A couple of things to remember:
    - Every animation scene is going to be a python `class` that derives the class `Scene`
    - The `construct` function under the class is the one that is executed for the animation
    - If you want to execute a specific scene `scene_name` out of multiple scenes (classes) defined in the same script file (`.py` file), then run the following in the terminal:
```bash
cd project/
manim -pql scene_file.py scene_name
```