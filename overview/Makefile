DRAFTPATH?=${HOME}/development/c++-standard-draft
SRC_PATH=${DRAFTPATH}/source

all : impldefcounts

impldefcounts: ${SRC_PATH}/numerics.tex
	@grep -c impldef ${SRC_PATH}/*tex|grep -v ':0'|csvsort-3 -H -d ':' -c 2|csvlook-3 -H
