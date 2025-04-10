#!/bin/bash


project="kanban"
uv run pytest --html=$test_html_path/$project.html
