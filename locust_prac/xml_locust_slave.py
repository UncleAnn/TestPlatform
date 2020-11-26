import os
os.system('locust -f xml_locust_master.py --worker --master-host=localhost')
