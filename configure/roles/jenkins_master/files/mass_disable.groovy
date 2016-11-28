for(item in hudson.model.Hudson.instance.items) {
  println("Disabling " + item.name)
  item.disabled = true
  item.save()
}
