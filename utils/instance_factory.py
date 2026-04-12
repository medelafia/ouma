from uuid import uuid4 
from schemas.schemas import Instance
from services.prometheus_service import fetch_instances

instances = None

def get_instances() : 
    global instances
    if instances is None : 
        print("value is none , loading from prometheus")
        instances = [Instance(instance_id=str(uuid4()), port=instance['labels']['instance'].split(":")[1], ip_address="localhost") for instance in fetch_instances()]
    else :
        print("value exists in memory")
    return instances 

def get_instance_by_id(id) :
    instances = get_instances()
    for instance in instances : 
        if instance.instance_id == id : 
            return instance
    return None


def get_instance_by_host_and_port(host , port) : 
    for instance in instances : 
        if instance.ip_address == host and instance.port == port : 
            return instance
    return None