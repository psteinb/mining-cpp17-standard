STD_PREFIX?=../../c++-standard-draft/
STD_TEX=$(STD_PREFIX)/source/std.tex

TEX_FILES=$(shell sed -n -e '103,132p' $(STD_TEX)|sed -e "s@.*{\(.*\)}@$(STD_PREFIX)/source/\1.tex@")

all: std.csv

std.csv: $(TEX_FILES)
	python3 ./impldef2csv.py -H -o "std.csv" $^

print:
	@echo $(TEX_FILES)

clean:
	@rm -vf std.csv
