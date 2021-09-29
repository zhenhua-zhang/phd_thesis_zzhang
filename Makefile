LATEXMK    := latexmk
LATEXFLAGS := -pdf -quiet

SRCDIR   = ./src
PDFDIR   = ./pdfs
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
	$(LATEXMK) ${LATEXFLAGS} -outdir=${BUILDDIR} $? 2>&1 1>/dev/null


# Clean-ups
clean:
	@echo Clean up...
	rm -fr ${BUILDDIR} ${PDFDIR}

clean-build:
	@echo Clean up...
	rm -fr ${BUILDDIR}


.PHONY: all clean
# vim: ts=4:
