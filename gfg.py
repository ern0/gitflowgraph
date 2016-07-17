#!/usr/bin/env python2
import sys
import os
from git import *


class GitFlowGraph:


	def main(self):

		try: self.repo = Repo(sys.argv[1])
		except:
			print("specify directory contains a repository")
			os._exit(2)

		self.nodes = {}

		for head in self.repo.heads:
			for refLogItem in head.log():
				node = Node()
				node.source = "reflog"
				node.branch = head.name
				node.hash = refLogItem.newhexsha
				node.prev = refLogItem.oldhexsha
				node.message = refLogItem.message
				node.store(self.nodes)

		for head in self.repo.heads:
			for commit in self.repo.iter_commits(head):
				node = Node()
				node.source = "commit"
				node.branch = None
				node.hash = commit.hexsha
				node.prev = None
				try: node.prev = commit.parents[0].hexsha
				except: pass
				node.message = commit.message
				node.store(self.nodes)

		for hash in self.nodes: 
			self.nodes[hash].dump()


class Node:

	def __init__(self):
		self.branches = {}


	def regBranch(self,branch):
		if branch == None: return
		self.branches[branch] = branch


	def store(self,nodes):

		self.message = self.message.replace("\n","")

		if self.source == "commit":
			self.type = "commit"
			self.aux = None
		else:
			self.type = self.message.split(":")[0].split(" ")[0]
			self.message = self.message[2 + self.message.index(":"):]

		if self.type not in ["commit","branch","merge"]: return

		if self.hash not in nodes: 
			nodes[self.hash] = self
			self.regBranch(self.branch)
			return

		node = nodes[self.hash]
		if self.source == "reflog": self.message = node.message
		if self.prev == None: self.prev = node.prev


	def dump(self):

		b = ""
		for branch in self.branches:
			b += " #" + branch

		p = ""
		if self.prev != None: p = "(" + self.prev[0:6] + ")" 

		print(
			self.type + 
			": " +
			self.hash[0:6] +
			p + 
			" - " + 
			self.message +
			b
		)


if __name__ == "__main__":
	GitFlowGraph().main()