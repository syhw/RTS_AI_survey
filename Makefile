all: 
	pdflatex survey
	bibtex survey
	pdflatex survey
clean:
	rm -rf *.aux *.blg *.log
