def hudson = hudson.model.Hudson.instance
def globalProps = hudson.globalNodeProperties
if(globalProps.size() != 1) {
    globalProps.replaceBy(
        [new hudson.slaves.EnvironmentVariablesNodeProperty()])
}
def props = globalProps.getAll(
    hudson.slaves.EnvironmentVariablesNodeProperty.class)
for (prop in props) {
    // add prop.envVars.put(key, value)
    %s
}
hudson.save()
