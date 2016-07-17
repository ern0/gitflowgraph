#!/usr/bin/env python2
import sys
import os
from git import *


class Node:

	def dump():
		pass


class GitFlowGraph:


	def main(self):

		try: self.repo = Repo(sys.argv[1])
		except:
			print("specify directory contains a repository")
			os._exit(2)

		self.nodes = {}

		for head in self.repo.heads:
			log = head.log()	
			print("---- " + head.name + "(" + str(len(log)) + ") ----")
			for refLogItem in log:
				node = Node()
				node.branch = head.name
				node.hash = refLogItem.newhexsha
				node.prev = refLogItem.oldhexsha
				node.message = refLogItem.message
				self.store(node)

		for head in self.repo.heads:
			for commit in self.repo.iter_commits(head):
				node = Node()
				node.branch = "???"
				node.hash = commit.hexsha
				node.prev = None
				node.message = commit.message
				self.store(node)

		for i in self.nodes:
			node = self.nodes[i]
			print(node.hash[0:7] + " - " + node.message.replace("\n",""))


	def store(self,node):

		if node.hash not in self.nodes: 
			self.nodes[node.hash] = node
		self.nodes[node.hash].message += " #" + node.branch


if __name__ == "__main__":
	GitFlowGraph().main()