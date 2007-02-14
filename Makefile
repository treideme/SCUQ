## The SCUQ Library 
## ----------------
## SCUQ = class library for the evaluation Sclar- and Complex-valued Uncertain
##        Quantities
##
## This is the main creation script, the following targets are implemented
##
## all:    Creates the entire documentation and performs a self-test
## clean:  Removes temporary files
## doc:    Creates the entire documentation
## backup: Create a backup
## dist:   Create a distribution package (includes sources only).
## test:   Run self-tests on the library

# Files that are deleted by invoking clean
TMP_FILES=doc.log scuq/*.pyc scuq/*.pyo doc/html doc/latex Examples/*.pyc \
	  Examples/*.pyo *.log

# Files and directories that are important for backups
IMP_FILES=doc doc.cfg Examples scuq make_latex.sh \
	  Makefile AUTHORS

# The souce files 
SOURCES=scuq/arithmetic.py scuq/cucomponents.py scuq/__init__.py \
	scuq/operators.py scuq/qexceptions.py scuq/quantities.py \
	scuq/si.py scuq/testcases.py scuq/units.py 

all: doc test

clean: 
	rm -rf $(TMP_FILES)

## Documentation related tags

doc/html/index.html:  doc.cfg $(SOURCES)
	doxygen doc.cfg

doc/latex/refman.pdf: doc/html/index.html
	sh ./make_latex.sh

doc: doc/html/index.html doc/latex/refman.pdf

## Backups

backup: clean
	tar cvjf `date +"%Y%m%d"`_backup.tar.bz2 $(IMP_FILES)

## Distribution related info
dist: clean
	tar cvjf `date +"%Y%m%d"`_dist.tar.bz2 $(SOURCES)
	
test: $(SOURCES)
	python scuq/testcases.py

	
#strip_cvs:
#	rm -rf CVS .cvsignore doc/CVS doc/.cvsignore Examples/CVS \
#	           Examples/.cvsignore scuq/CVS 
