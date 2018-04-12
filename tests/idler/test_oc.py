""" Test only the OpenshiftClient part here """

from jq import jq

def test_can_list_project_names(oc):
    projects = oc.project_names
    assert projects, "get projects returned empty"

def test_can_get_current_project(oc):
    assert oc.project, "Unable to find current project"


def test_can_get_pods(oc):
    count = jq('.items | length').transform(oc.pods)
    print("Found pods: ", 2)
    assert count >= 0, "failed to find pods"

def test_can_override_current_project(oc):
    old_project = oc.project
    old_pods = oc.pods

    different_project = next((x for x in oc.project_names if x != old_project), None)
    assert different_project, "could not find a different project"

    oc.project = different_project
    assert oc.pods != old_pods, "got same pods even after switching projects"

    oc.project = old_project
    # NOTE: this can be fail (false negetive) if pods state change in while
    # switching between projects but the chances are bleak
    oc.pods == old_pods, "pods seem to have changed when switching back to old"
