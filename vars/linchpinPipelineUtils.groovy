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
}
