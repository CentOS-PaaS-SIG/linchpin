import org.centos.pipeline.LinchpinPipelineUtils

/**
 * A class of methods used in the Jenkinsfile pipeline.
 *
 */

class linchpinPipelineUtils implements Serializable {

    def linchpinPipelineUtils = new LinchpinPipelineUtils()

    def getTargetsToTest(targetsMap) {
        return linchpinPipelineUtils.getTargetsToTest(targetsMap)
    }

    def getProvidersToTest(providersMap) {
        return linchpinPipelineUtils.getProvidersToTest(providersMap)
    }

    def sendPRComment(ghprbGhRepository, ghprbPullId, message) {
        return linchpinPipelineUtils.sendPRComment(ghprbGhRepository, ghprbPullId, message)
    }

    def getChangedFile(filePath){
        return linchpinPipelineUtils.sendPRComment(filePath)
    }
}
