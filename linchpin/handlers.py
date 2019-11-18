def handler_assign_async_value(pbar, msg, index, resources):
    pbar.postfix[0]['state']='Linchpin initializing'
    pbar.update()
    return index

def handler_get_the_resource_name(pbar, msg, index, resources):
    pbar.postfix[0]['state'] = 'Provisioning started'
    pbar.postfix[0]['name'] = resources[index]
    pbar.update()
    return index

def handler_add_types_to_resource(pbar, msg, index, resources):
    pbar.postfix[0]['state']='Provisioned'
    return index + 1

def handler_wait_on_jobs(pbar, msg, index, resources):
    pbar.postfix[0]['state']='Linchpin results processing'
    pbar.postfix[0]['name'] = ''
    pbar.update()
    return index

def handler_done(pbar, msg, index, resources):
    pbar.postfix[0]['state']='Done'
    return index
