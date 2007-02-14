#!/bin/sh

pushd doc/latex
pdflatex refman
pdflatex refman
popd
