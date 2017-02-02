import json
import pdb
import getopt
import sys
import logging
import os

#filepath = "/Users/pmenon/Automation/gerrit/qe_ifra/qe-infra/linux/nightlies/IBM-2.6-Secure.json"

USAGE = '''

INCORRECT USAGE 
USAGE : python jsonpar.py -p <path to json file> [-d]


'''

logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
logger = logging.getLogger("JSON PARSER")
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler(stream=sys.stdout)
ch.setFormatter(logFormatter)
logger.addHandler(ch)
logger.info ("Starting Program")

def main():
	try:
		debug = False
		fp = False
		opts, args = getopt.getopt(sys.argv[1:],"p:d",[])
		for k,v in opts:
			if k == "-p":
				filepath = v
				fp =True	
				if not os.path.isfile(filepath):
					logger.debug("%s does not exist" %(filepath))
					exit(0)
					
			if k == "-d":
				debug = True
	except:
		print USAGE
		exit(0)
	
	if not fp:
		print USAGE
		exit(0)
        logger.info("Processing file : %s" %(filepath))	
	if debug:	
		ch.setLevel(logging.DEBUG)
	else:
		ch.setLevel(logging.INFO)
	retHash = json.load(open(filepath))
	resultHash={}
	for key,value in retHash.iteritems():
		num_of_cluster = 1
		if "num_of_clusters" in retHash[key]["override_properties"]:
			num_of_cluster = retHash[key]["override_properties"]["num_of_clusters"]
		total_machines = int(num_of_cluster) * int(retHash[key]["number_of_nodes"]) * int(retHash[key]["number_of_splits"])
		logger.debug("{0} --- {1}".format(key,total_machines))
		if retHash[key]["override_properties"]["STORAGE_CONSOLE"] in resultHash:
			resultHash[retHash[key]["override_properties"]["STORAGE_CONSOLE"]] = int(resultHash[retHash[key]["override_properties"]["STORAGE_CONSOLE"]]) + total_machines
		else:
			resultHash[retHash[key]["override_properties"]["STORAGE_CONSOLE"]] = total_machines

	for key, value in resultHash.iteritems():
		logger.info("{0} --- {1}".format(key,value))
		#print key, value

if __name__ == "__main__":
	main()

