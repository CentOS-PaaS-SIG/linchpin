#!/bin/bash

# set to 1 to enable debugging
DEBUG=0

## Openshift Project. Will get created if it does not exist
project="continuous-infra"

## List all templates to be processed
templates="jenkins/jenkins-continuous-infra-slave-buildconfig-template.yaml \
    jenkins/jenkins-persistent-buildconfig-template.yaml \
    jenkins/buildah-buildconfig-template.yaml \
    distros/centos7-buildconfig-template.yaml \
    distros/fedora29-buildconfig-template.yaml \
    distros/fedora28-buildconfig-template.yaml"

function logerror {
  echo "Error: $1"
  exit 1
}

function logwarning {
  echo "Warning: $1"
}

function logdebug {
  if [ ${DEBUG} -eq 1 ] ; then
    echo "DEBUG: $1"
  fi
}

function loginfo {
  echo "$1"
}

function verifyEnv {
  ## jq
  command -v jq >/dev/null 2>&1 || { echo "Require jq but it's not installed.  Aborting." >&2; exit 1; }
  ## oc
  command -v oc >/dev/null 2>&1 || { echo "Require oc but it's not installed.  Aborting." >&2; exit 1; }
}

function processTemplate {
    templateFile="${1}"
    loginfo "* Processing ${templateFile}..."
    templateName=$(oc process -f "${templateFile}" | jq '.items[1].metadata.labels.template' | sed 's/"//g')
    logdebug "  - Template name is ${templateName}"
    imageStreamName=$(oc process -f "${templateFile}" | jq '.items[0].metadata.name' | sed 's/"//g')
    logdebug "  - ImageStream name is ${imageStreamName}"
    buildConfigName=$(oc process -f "${templateFile}" | jq '.items[1].metadata.name' | sed 's/"//g')
    logdebug "  - Build Config name is ${buildConfigName}"

    oc get template "${templateName}" > /dev/null 2>&1

    if [ $? -ne 0 ] ; then
        loginfo "    >> Creating Build Config Template ${templateName}"
        oc create -f "${templateFile}" > /dev/null 2>&1 || { echo "Failed to create build config! Aborting." >&2; exit 1; }
    else
        logdebug "    >> Updating Build Config Template ${templateName}"
        oc replace -f "${templateFile}" > /dev/null 2>&1 || { echo "Failed to update build config! Aborting." >&2; exit 1; }
    fi

    imageExists=0
    oc get imagestream "${imageStreamName}" > /dev/null 2>&1
    if [ $? -eq 0 ] ; then
        logdebug "    Image Stream ${imageStreamName} already exists"
        imageExists=1
    fi
    buildConfigExists=0
    oc get buildconfig "${buildConfigName}" > /dev/null 2>&1
    if [ $? -eq 0 ] ; then
        logdebug "    Build Config ${buildConfigName} already exists"
        buildConfigExists=1
    fi

    if [[ ${imageExists} -eq 0 ]] && [[ ${buildConfigExists} -eq 0 ]] ; then
        loginfo "    >> Image Stream and Build Config do not exist. Creating..."
        oc new-app "${templateName}" ${REPO_URL_PARAM} ${REPO_REF_PARAM} > /dev/null 2>&1 || { echo "Failed to create new app! Aborting." >&2; exit 1; }
    fi
    loginfo ""
}

##
verifyEnv

loginfo ""

if [ -z "${REPO_URL}" ] ; then
  REPO_URL_PARAM=""
else
  REPO_URL_PARAM="-p REPO_URL=${REPO_URL}"
fi
##
if [ -z "${REPO_REF}" ] ; then
  REPO_REF_PARAM=""
else
  REPO_REF_PARAM="-p REPO_REF=${REPO_REF}"
fi

oc project "${project}" > /dev/null 2>&1
if [ $? -ne 0 ] ; then
  logdebug "Project does not exist...Creating..."
  oc new-project "${project}" > /dev/null 2>&1 || { echo "Failed to create new project! Aborting." >&2; exit 1; }
  oc project "${project}" > /dev/null 2>&1
fi

for template in ${templates[@]}; do
    processTemplate "${template}"
done

loginfo "Done!"
