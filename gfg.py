#!/usr/bin/env python2
import sys
import os
import datetime
from git import *


class GitFlowGraph:


	def main(self):

		try: self.repo = Repo(sys.argv[1])
		except:
			print("specify directory contains a repository")
			os._exit(2)

		self.nodeList = {}

		for head in self.repo.heads:
			branch = head.name
			for refLogItem in head.log():

				isCommit = False
				if refLogItem.message.startswith("commit"): isCommit = True
				if refLogItem.message.startswith("commit (merge)"): isCommit = False
				if not isCommit: continue 

				node = Node()
				node.hash = refLogItem.newhexsha
				node.branch = branch
<<<<<<< HEAD
				node.message = refLogItem.message.strip()
=======
				node.message = "//" + refLogItem.message.strip()
>>>>>>> ec01ac953d1a18d91e84ca23fb4be327a9e95f32
				tm = refLogItem.time[0]
				tz = refLogItem.time[1]
				node.stamp = str(datetime.datetime.utcfromtimestamp(tm - tz))

				self.nodeList[node.hash] = node

			for commit in self.repo.iter_commits(head):
				
				try: 
					node = self.nodeList[commit.hexsha]
				except:
					node = Node()
					self.nodeList[commit.hexsha] = node
<<<<<<< HEAD
					node.branch = branch
=======
					node.branch = branch + "?"
>>>>>>> ec01ac953d1a18d91e84ca23fb4be327a9e95f32

				node.hash = commit.hexsha
				node.message = commit.message.strip()
				plus = str(commit.committed_datetime).index("+")
				node.stamp = str(commit.committed_datetime)[0:plus]

		for key in (
			sorted(
				self.nodeList.keys()
				,key = lambda h: self.nodeList[h].stamp
				,reverse = True
			)
		):
			self.nodeList[key].dump()


class Node:


	# columns: feat(1) develop(3) release(5) master(7) hotfix(9) 
	def getColumn(self):		
		if self.branch.startswith("devel"): return 3
		if self.branch.startswith("rel"): return 5
		if self.branch.startswith("master"): return 7
		if self.branch.startswith("hotfix"): return 9
		return 1  # feat


	def dump(self):

		print(
			self.hash[0:6] + "..."
			+ " - \"" + self.message + "\""
			+ " - #" + self.branch
			+ " - " + self.stamp
			+ " - [" + str(self.getColumn()) + "]"
		)


if __name__ == "__main__":
	GitFlowGraph().main()