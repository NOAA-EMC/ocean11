#!/bin/bash

# export CONFIG_DIR="./config"


echo "set environment parameters"
# export RUN_ENVIR=emc
export HOMEgfs="/work/noaa/da/edwardg/01142025/global-workflow"
echo "HOMEgfs=${HOMEgfs}"

# PDY=<cyclestr>@Y@m@d</cyclestr>
# export PDY=$(date +"%Y%m%d")
export PDY=20230630
echo "PDY=${PDY}"

# cyc=<cyclestr>@H</cyclestr>
# export cyc=$(date +"%H")
export cyc=00
echo "cyc=${cyc}"

# from config.base
export assim_freq=6
# RUN</name><value>gdas</value></envar>
export RUN=gdas
export SOCA_INPUT_FIX_DIR=/work/noaa/da/edwardg/01142025/global-workflow/fix/gdas/soca/72x35x25/soca
# export DATA=/work/noaa/stmp/edwardg/HERCULES/RUNDIRS/C48mx500_3DVarAOWCDA/gdas.2021032500/prepoceanobs.1076207
export DATA=./data


# source config.prepoceanobs
# from config.prepoceanobs
# export OBS_YAML=/work/noaa/da/edwardg/01142025/global-workflow/parm/gdas/soca/obs/obs_list.yaml
export OBS_YAML=./config/obs_list.yaml
# export MARINE_OBS_YAML_DIR=/work/noaa/da/edwardg/01142025/global-workflow/parm/gdas/soca/obs/config
export MARINE_OBS_YAML_DIR=./config/marine_obs_yaml_dir
# export OBSPREP_YAML=/work/noaa/da/edwardg/01142025/global-workflow/parm/gdas/soca/obsprep/obsprep_config.yaml
export OBSPREP_YAML=./config/obsprep_config.yaml

# from JGLOBAL_PREP_OCEAN_OBS
# export COMIN_OBS=/work/noaa/stmp/edwardg/HERCULES/RUNDIRS/C48mx500_3DVarAOWCDA/gdas.2021032500/prepoceanobs.1076207
export COMIN_OBS=./data
# declare_from_tmpl :: COMOUT_OBS=/work/noaa/da/edwardg/01142025/global-workflow/sorc/gdas.cd/build/gdas/test/gw-ci/../../test/gw-ci/C48mx500_3DVarAOWCDA/COMROOT/C48mx500_3DVarAOWCDA/gdas.20210325/00/obs
export COMOUT_OBS=./output

# from config.base
# export DMPDIR=/work/noaa/rstprod/dump
export DMPDIR=/work/noaa/da/marineda/gfs-marine/data/obs/

# from config.prepoceanobs
export OCNOBS2IODAEXEC=${HOMEgfs}/sorc/gdas.cd/build/bin/gdas_obsprovider2ioda.x


# pyiodaPATH="${HOMEgfs}/sorc/gdas.cd/build/lib/python$(detect_py_ver)/"
pyiodaPATH="${HOMEgfs}/sorc/gdas.cd/build/lib/python3.7/"
PYTHONPATH="${pyiodaPATH}:${PYTHONPATH}"
export PYTHONPATH
echo "set PYTHONPATH = ${PYTHONPATH}"



echo "loading modules"
. "${HOMEgfs}/ush/load_ufsda_modules.sh"
echo "finished loading modules"

echo "executing python prep_ocean_obs"
export MARINE_OBSPREP_DIR="/home/edwardg/prepoceanobs/marine_obsprep"
# ${MARINE_OBSPREP_DIR}/exglobal_prep_ocean_obs.py
${MARINE_OBSPREP_DIR}/run_prep_ocean_obs.py -c y.yaml
echo "done executing python prep_ocean_obs"
exit

echo "NNNNNNNNNNNNNNN"





CYCLE=202103250000
task=gdas_prepoceanobs
workflow_name=C48mx500_3DVarAOWCD

workflow_xml=C48mx500_3DVarAOWCDA.xml
contents:
--------


        <command>/work/noaa/da/edwardg/01142025/global-workflow/jobs/rocoto/prepoceanobs.sh</command>

--------------------------------------
# setup the environment:

EXPDIR</name><value>/work/noaa/da/edwardg/01142025/global-workflow/sorc/gdas.cd/build/gdas/test/gw-ci/../../test/gw-ci/C48mx500_3DVarAOWCDA/EXPDIR/C48mx500_3DVarAOWCDA
NET</name><value>gfs</value></envar>
CDATE</name><value><cyclestr>@Y@m@d@H</cyclestr></value></envar>
COMROOT=/work/noaa/da/edwardg/01142025/global-workflow/sorc/gdas.cd/build/gdas/test/gw-ci/../../test/gw-ci/C48mx500_3DVarAOWCDA/COMROOT
DATAROOT=/work/noaa/stmp/edwardg/HERCULES/RUNDIRS/C48mx500_3DVarAOWCDA/gdas.<cyclestr>@Y@m@d@H</cyclestr>

/work/noaa/da/edwardg/01142025/global-workflow/jobs/rocoto/prepoceanobs.sh


source "${HOMEgfs}/ush/preamble.sh"

###############################################################
# Source UFSDA workflow modules
. "${HOMEgfs}/ush/load_ufsda_modules.sh"
status=$?
[[ ${status} -ne 0 ]] && exit "${status}"

export job="prepoceanobs"
export jobid="${job}.$$"

###############################################################
# Execute the JJOB
# "${HOMEgfs}"/jobs/JGLOBAL_PREP_OCEAN_OBS

# source "${HOMEgfs}/ush/preamble.sh"
# source "${HOMEgfs}/ush/jjob_header.sh" -e "prepoceanobs" -c "base prepoceanobs"


export COMIN_OBS="${DATA}"
YMD=${PDY} HH=${cyc} declare_from_tmpl -rx COMOUT_OBS:COM_OBS_TMPL
exglobal_prep_ocean_obs.py

