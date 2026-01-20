ROOTDIR=$(realpath $(dir $(firstword $(MAKEFILE_LIST))))


SRCDIR=${ROOTDIR}/rpi_gyro_reader
INSTALL_LOG_FILE=${ROOTDIR}/install.log
VENV_SUBDIR=${ROOTDIR}/venv


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
	${ACTIVATE}; ${PYTHON} -m ${PIP} install -e ${ROOTDIR}[rpi] --prefer-binary --log ${INSTALL_LOG_FILE}
	touch $@

clean_install_rpi:
	rm -f install_rpi

clean_install:
	rm  -f install

install: ${VENV_SUBDIR}
	${ACTIVATE}; ${PYTHON} -m ${PIP} install -e ${ROOTDIR} --prefer-binary --log ${INSTALL_LOG_FILE}
	touch $@

$(VENV_SUBDIR):
	${SYSPYTHON} -m venv --upgrade-deps ${VENV_OPTIONS} ${VENV_SUBDIR}
	

read_gyro: install_rpi
	@echo "Reading gyro"
	${ACTIVATE}; read_gyro

clean: clean_install clean_install_rpi
	rm -rf ${VENV_SUBDIR}
