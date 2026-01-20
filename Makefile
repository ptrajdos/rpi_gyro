ROOTDIR=$(realpath $(dir $(firstword $(MAKEFILE_LIST))))


SRCDIR=${ROOTDIR}/rpi_gyro_reader
TESTDIR=${ROOTDIR}/tests
INSTALL_LOG_FILE=${ROOTDIR}/install.log
VENV_SUBDIR=${ROOTDIR}/venv

COVERAGE = coverage
UNITTEST_PARALLEL = unittest-parallel
PDOC= pdoc3
PYTEST=pytest

PYTHON=python
SYSPYTHON=python
PIP=pip

LOGDIR=${ROOTDIR}/testlogs
LOGFILE=${LOGDIR}/`date +'%y-%m-%d_%H-%M-%S'`.log

VENV_OPTIONS=

ifeq ($(OS),Windows_NT)
	ACTIVATE:=. ${VENV_SUBDIR}/Scripts/activate
else
	ACTIVATE:=. ${VENV_SUBDIR}/bin/activate
endif


.PHONY: all clean test docs

all: read_gyro

install_rpi:  ${VENV_SUBDIR}
	${ACTIVATE}; ${PYTHON} -m ${PIP} install -e ${ROOTDIR}[rpi,test] --prefer-binary --log ${INSTALL_LOG_FILE}
	touch $@

clean_install_rpi:
	rm -f install_rpi

clean_install:
	rm  -f install

install: ${VENV_SUBDIR}
	${ACTIVATE}; ${PYTHON} -m ${PIP} install -e ${ROOTDIR}[test] --prefer-binary --log ${INSTALL_LOG_FILE}
	touch $@

$(VENV_SUBDIR):
	${SYSPYTHON} -m venv --upgrade-deps ${VENV_OPTIONS} ${VENV_SUBDIR}
	

read_gyro: install_rpi
	@echo "Reading gyro"
	${ACTIVATE}; read_gyro

clean: clean_install clean_install_rpi
	rm -rf ${VENV_SUBDIR}


test: install
	mkdir -p ${LOGDIR}  
	${ACTIVATE}; ${COVERAGE} run --branch  --source=${SRCDIR} -m unittest discover -p '*_test.py' -v -s ${TESTDIR} 2>&1 |tee -a ${LOGFILE}
	${ACTIVATE}; ${COVERAGE} html --show-contexts


test_parallel: install
	mkdir -p ${COVDIR} ${LOGDIR}
	${ACTIVATE}; ${UNITTEST_PARALLEL} --class-fixtures -v -t ${ROOTDIR} -s ${TESTDIR} -p '*_test.py' --coverage --coverage-rcfile ./.coveragerc --coverage-source ${SRCDIR} --coverage-html ${COVDIR}  2>&1 |tee -a ${LOGFILE}

docs: install
	${ACTIVATE}; $(PDOC) --force --html ${SRCDIR} --output-dir ${DOCS_DIR}

profile: install
	
	${ACTIVATE}; ${PYTEST} -n auto --cov-report=html --cov=${SRCDIR} --profile ${TESTDIR}