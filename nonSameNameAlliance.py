from maya import cmds
import re


def rerename(node_uuid):
    for node in cmds.ls(node_uuid):
        if "|" in node:
            basename = re.search("^(.+)?\|(.+?)(\d+)?$", node).group(2)
            rename_name = cmds.rename(node, "{}#".format(basename))

def renameEvent():
    try:
        rename = {}
        for node_uuid in cmds.ls(cmds.ls(sl=True), uuid=True):
            rerename(node_uuid)

    except Exception as e:
        sys.stderr.write(str(e))
        
def duplicateEvent():
    try:
        rename = {}
        for node_uuid in cmds.ls(cmds.ls(sl=True, dag=True, tr=True), uuid=True):
            rerename(node_uuid)

    except Exception as e:
        sys.stderr.write(str(e))

def main():
    
    try:
        if jobIds:
            for jobId in jobIds:
                cmds.scriptJob(kill=jobId, force=True)
            jobIds = []
    except:
        jobIds = []
    
    jobIds.append(cmds.scriptJob(event=["NameChanged", renameEvent], protected=True))
    jobIds.append(cmds.scriptJob(event=["SelectionChanged", duplicateEvent], protected=True))
