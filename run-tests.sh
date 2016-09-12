#!/bin/sh

set -e

echo "----Running flake8----"
flake8 ai_graph_color tests

echo "----Running nosetests----"
nosetests tests
