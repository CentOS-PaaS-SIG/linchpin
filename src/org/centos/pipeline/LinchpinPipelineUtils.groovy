#!/usr/bin/groovy
package org.centos.pipeline

def keysToList(keyValue) {
    // Convert map keys to list
    keys = []
    keyValue.each { key, value ->
        keys.add(key)
    }
    return keys
}

def matchPath(path, paths){
    for (int i = 0; i < paths.size(); i++) {
        if (path ==~ ~/${paths[i]}/) {
            return true
        }
    }
    return false
}

def getTargetsToTest(targetsMap) {
    def targets = [:]
    def changeLogSets = currentBuild.changeSets
    for (int i = 0; i < changeLogSets.size(); i++) {
        def entries = changeLogSets[i].items
        for (int j = 0; j < entries.length; j++) {
            def entry = entries[j]
            def files = new ArrayList(entry.affectedFiles)
            for (int k = 0; k <files.size(); k++) {
                def this_match = false
                def file = files[k]
                for (e in targetsMap) {
                    if (matchPath(file.path, e.value)) {
                        println "${e.key} matched ${file.path}"
                        this_match = true
                        targets[e.key] = 1
                    }
                }
                if (!this_match) {
                    // If we get here then we have a non-target specific change
                    // and all targets should be tested.
                    println "Non-target file matched, will test all targets"
                    return keysToList(targetsMap)
                }
            }
        }
    }
    return keysToList(targets)
}

def getProvidersToTest(providersMap) {
    def providers = [:]
    def changeLogSets = currentBuild.changeSets
    for (int i = 0; i < changeLogSets.size(); i++) {
        def entries = changeLogSets[i].items
        for (int j = 0; j < entries.length; j++) {
            def entry = entries[j]
            def files = new ArrayList(entry.affectedFiles)
            for (int k = 0; k <files.size(); k++) {
                def this_match = false
                def file = files[k]
                for (e in providersMap) {
                    if (matchPath(file.path, e.value)) {
                        println "${e.key} matched ${file.path}"
                        this_match = true
                        targets[e.key] = 1
                    }
                }
                if (!this_match) {
                    // If we get here then we have a non-target specific change
                    // and all targets should be tested.
                    println "Non-target file matched, will test all targets"
                    return keysToList(providersMap)
                }
            }
        }
    }
    return keysToList(providers)
}

def sendPRComment(ghprbGhRepository, ghprbPullId, msg) {
    if (msg == null) {
        return
    }
    println "Prepare GHI tool"
    withCredentials([string(credentialsId: 'paas-bot', variable: 'TOKEN')]) {
        sh "git config --global ghi.token ${TOKEN}"
        sh 'curl -sL https://raw.githubusercontent.com/stephencelis/ghi/master/ghi > ghi && chmod 755 ghi'
        sh './ghi comment ' + ghprbPullId + ' -m "' + msg + '" -- ' + ghprbGhRepository
    }
}
