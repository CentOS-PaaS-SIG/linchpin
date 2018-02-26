import java.util.logging.Logger
import jenkins.security.s2m.*
import jenkins.model.*;
import com.redhat.jenkins.plugins.ci.*
import com.redhat.jenkins.plugins.ci.messaging.*
import hudson.markup.RawHtmlMarkupFormatter
import hudson.model.*
import hudson.security.*
import com.cloudbees.plugins.credentials.*
import com.cloudbees.plugins.credentials.common.*
import com.cloudbees.plugins.credentials.domains.*
import com.cloudbees.plugins.credentials.impl.*
import org.jenkinsci.plugins.plaincredentials.*
import org.jenkinsci.plugins.plaincredentials.impl.*
import org.apache.commons.fileupload.* 
import org.apache.commons.fileupload.disk.*
import java.nio.file.Files

def logger = Logger.getLogger("")
logger.info("Disabling CLI over remoting")
jenkins.CLI.get().setEnabled(false);
logger.info("Enable Slave -> Master Access Control")
Jenkins.instance.injector.getInstance(AdminWhitelistRule.class).setMasterKillSwitch(false);
// Set global and job read permissions
def strategy = new GlobalMatrixAuthorizationStrategy()
strategy.add(hudson.model.Hudson.READ,'anonymous')
strategy.add(hudson.model.Item.READ,'anonymous')
Jenkins.instance.setAuthorizationStrategy(strategy)
// Set Markup Formatter to Safe HTML so PR hyperlinks work
Jenkins.instance.setMarkupFormatter(new RawHtmlMarkupFormatter(false))
Jenkins.instance.save()

logger.info("Setup fedora-fedmsg Messaging Provider")
FedMsgMessagingProvider fedmsg = new FedMsgMessagingProvider("fedora-fedmsg", "tcp://hub.fedoraproject.org:9940", "tcp://172.19.4.24:9941", "org.fedoraproject");
GlobalCIConfiguration.get().addMessageProvider(fedmsg)

logger.info("Setup fedora-fedmsg-stage Messaging Provider")
FedMsgMessagingProvider fedmsgStage = new FedMsgMessagingProvider("fedora-fedmsg-stage", "tcp://stg.fedoraproject.org:9940", "tcp://172.19.4.36:9941", "org.fedoraproject");
GlobalCIConfiguration.get().addMessageProvider(fedmsgStage)

logger.info("Setup fedora-fedmsg-devel Messaging Provider")
FedMsgMessagingProvider fedmsgDevel = new FedMsgMessagingProvider("fedora-fedmsg-devel", "tcp://fedmsg-relay.continuous-infra.svc:4001", "tcp://fedmsg-relay.continuous-infra.svc:2003", "org.fedoraproject");
GlobalCIConfiguration.get().addMessageProvider(fedmsgDevel)

logger.info("Setting Time Zone to be EST")
System.setProperty('org.apache.commons.jelly.tags.fmt.timeZone', 'America/New_York')

// Add global variable
instance = Jenkins.getInstance()
globalNodeProperties = instance.getGlobalNodeProperties()
envVarsNodePropertyList = globalNodeProperties.getAll(hudson.slaves.EnvironmentVariablesNodeProperty.class)

newEnvVarsNodeProperty = null
envVars = null

if ( envVarsNodePropertyList == null || envVarsNodePropertyList.size() == 0 ) {
  newEnvVarsNodeProperty = new hudson.slaves.EnvironmentVariablesNodeProperty();
  globalNodeProperties.add(newEnvVarsNodeProperty)
  envVars = newEnvVarsNodeProperty.getEnvVars()
} else {
  envVars = envVarsNodePropertyList.get(0).getEnvVars()

}

// This is the default for minishift.  You may need to change this
// for other environments.
envVars.put("DOCKER_REPO_URL", "172.30.1.1:5000")
instance.save()

domain = Domain.global()
store = Jenkins.instance.getExtensionList('com.cloudbees.plugins.credentials.SystemCredentialsProvider')[0].getStore()

factory = new DiskFileItemFactory()
dfi = factory.createItem("", "application/octet-stream", false, "filename")
out = dfi.getOutputStream()
file = new File("/dev/null")
Files.copy(file.toPath(), out)
// FileCredentailsImpl can take a file from a do
secretFile = new FileCredentialsImpl(
CredentialsScope.GLOBAL,
"duffy-key",
"Empty Duffy Key",
dfi, // Don't use FileItem
"",
"")
store.addCredentials(domain, secretFile)
