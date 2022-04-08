LATEXMK     := latexmk
LATEX_FLAGS := -pdf -quiet

PANDOC         := pandoc
PANDOC_FLAGS   := --from latex+raw_tex
PANDOC_FILTERS := ./misc/tikz.lua

SRCDIR   = ./src
PDFDIR   = ./pdfs
DOCDIR   = ./docs
BUILDDIR = ./build

SRCFILES = $(wildcard ${SRCDIR}/*.tex)
PDFFILES = $(SRCFILES:${SRCDIR}/%.tex=%.pdf)

# Generate *.pdf from ${SRCDIR}/*.tex and copy *.pdf to ${PDFDIR}
all: ${PDFFILES}
	@echo Collecting pdf generated from all tex files...

	@mkdir -p ${PDFDIR}
	@cp ./${BUILDDIR}/*.pdf ${PDFDIR}

	@echo Check ${BUILDDIR} for intermidiate files.
	@echo Check ${PDFDIR} for all created pdf files.


# Generate given .pdf, then copy it to ${PDFDIR}.
%: %.pdf
	@echo Making $@ from $?...

	@mkdir -p ${PDFDIR}
	@cp ./${BUILDDIR}/*.pdf ${PDFDIR}


# Generate .pdf from the corresponding .tex file.
%.pdf: src/%.tex
	@echo Making $@ from $?...

	@mkdir -p ./${BUILDDIR}
	$(LATEXMK) ${LATEX_FLAGS} -outdir=${BUILDDIR} $? 2>&1 1>/dev/null


# Generate .docx from the .tex file.
%.docx: src/%.tex
	@echo Making $@ from $?...

	@mkdir -p ${BUILDDIR} ${DOCDIR}
	$(PANDOC) ${PANDOC_FLAGS} --lua-filter=${PANDOC_FILTERS} -o ${DOCDIR}/$@ $?


# Clean-ups
clean-build:
	@echo Clean up...
	rm -fr ${BUILDDIR}

clean-pdf:
	@echo Clean up pdfs...
	rm -fr ${PDFDIR}

clean-doc:
	@echo Clean ip docs...
	rm -fr ${DOCDIR}

clean-all: clean-build clean-pdf clean-doc
	@echo Clean up...


.PHONY: all clean-all clean-build clean-doc clean-pdf
# vim: ts=4:
