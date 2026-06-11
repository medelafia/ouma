from uuid import uuid4 
from schemas.schemas import Instance
from services.prometheus_service import fetch_instances
from services.instances_services import load_instance_by_host_and_port , save_instance
import logging

logger = logging.getLogger(__name__)
instances = None



def get_instances() : 
    global instances
    if instances is None : 
        logger.info("instances data is none , loading from prometheus")
        data = []
        print(fetch_instances())
        for instance in fetch_instances() : 
            try :
                host = instance['labels']['instance'].split(":")[0]
                port = int(instance['labels']['instance'].split(":")[1])
                founded_instance = load_instance_by_host_and_port(host , port ) 

                if founded_instance is not None : 
                    print("INFO:loading instance data from the database for fast access")
                    data.append(Instance(instance_id=founded_instance[0], port=port, ip_address=host , cpu_usage=None, memory_usage=None))
                else : 
                    print("instance not found in the database")
                    new_instance = Instance(instance_id=str(uuid4()), port=port, ip_address=host, cpu_usage=None, memory_usage=None)
                    data.append(new_instance)
                    save_instance(new_instance)
            except Exception as ex : 
                print(ex)
        instances = data[::] 
    else :
        logger.info("Instances data exists in cache")
    return instances 

def get_instance_by_id(id) :
    instances = get_instances()
    for instance in instances : 
        if instance.instance_id == id : 
            return instance
    return None


def get_instance_by_host_and_port(host , port) : 
    for instance in get_instances() : 
        if instance.ip_address == host and instance.port == int(port) : 
            return instance
    return None