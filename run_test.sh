#!/bin/bash

#pytest-html

project="kanbanz"
uv run pytest --html=$test_html_path/$project.html
