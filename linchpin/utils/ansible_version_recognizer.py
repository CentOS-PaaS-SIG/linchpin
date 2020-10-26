import ansible

ansible_ver_firstdigit = int(ansible.__version__.split('.')[:2][0])
ansible_ver_seconddigit = int(ansible.__version__.split('.')[:2][1])
ansible_version = [ansible_ver_firstdigit, ansible_ver_seconddigit]


def ansibleverisgreaterthan(comparedversion):
    # compareversion is the version you want to
    # compare with the currrent ansible version
    versions = str(comparedversion).split(".")
    if ansible_version[0] > int(versions[0]):
        return True
    if ansible_version[0] == int(versions[0]) and\
            ansible_version[1] > int(versions[1]):
        return True
    return False
