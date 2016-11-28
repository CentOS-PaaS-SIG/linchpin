def hudson = hudson.model.Hudson.instance

hudson.setNumExecutors(10)

def ds = hudson.getExtensionList(jenkins.model.DownloadSettings.class)[0]
ds.setUseBrowser(false)
ds.save()
