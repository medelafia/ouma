from uuid import uuid4 
from schemas.schemas import Instance
from services.prometheus_service import fetch_instances
from services.instances_services import load_instance_by_host_and_port , save_instance
instances = None

def get_instances() : 
    global instances
    if instances is None : 
        print("value is none , loading from prometheus")
        data = []
        print(fetch_instances())
        for instance in fetch_instances() : 
            try :
                host = instance['labels']['instance'].split(":")[0]
                port = int(instance['labels']['instance'].split(":")[1])
                founded_instance = load_instance_by_host_and_port(host , port ) 

                if founded_instance is not None : 
                    print("loading instance from the data base for fast access")
                    data.append(Instance(instance_id=founded_instance[0], port=port, ip_address=host))
                else : 
                    print("instance not found in the database")
                    new_instance = Instance(instance_id=str(uuid4()), port=port, ip_address=host)
                    data.append(new_instance)
                    save_instance(new_instance)
            except Exception as ex : 
                print(ex)
        print(data)
        instances = data[::] 
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
    for instance in get_instances() : 
        if instance.ip_address == host and instance.port == port : 
            return instance
    return None