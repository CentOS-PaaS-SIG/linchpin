import os
import xml.etree.ElementTree as ET
from ansible.module_utils.basic import AnsibleModule

# replace default update center with our own
def set_default(tree, url):
    default_update_center = tree.find(".//site[id='default']")
    if default_update_center is None:
        raise Exception('Default update center not found')
    new_url = default_update_center.find('url')
    if new_url.text != url:
        new_url.text = url
        return True
    return False

# append additional update centers
def append(tree, site_id, url):
    xpath = './/site[id="{0}"]'.format(site_id)
    check_existing = tree.find(xpath)
    if check_existing is None:
        # Append if not found
        for sites in tree.iter('sites'):
            site = ET.Element('site')
            new_site_id = ET.SubElement(site, 'id')
            new_site_id.text = site_id
            new_url = ET.SubElement(site, 'url')
            new_url.text = url
            sites.append(site)
        return True
    else:
        # Update URL if necessary
        if check_existing.text != url:
            check_existing.text = url
            return True
        return False

def main():
    module = AnsibleModule(
        argument_spec={
            'jenkins_home': {'default': '/var/lib/jenkins'},
            'update_center_id': {'required': True},
            'update_center_url': {'required': True}
        }
    )
    update_ctr_config = os.path.join(module.params['jenkins_home'], 'hudson.model.UpdateCenter.xml')
    tree = ET.parse(update_ctr_config)
    if module.params['update_center_id'] == 'default':
        changed = set_default(tree, module.params['update_center_url'])
    else:
        changed = append(tree, module.params['update_center_id'], module.params['update_center_url'])
    tree.write(update_ctr_config, encoding='UTF-8')
    module.exit_json(changed=changed)

main()
