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

		self.nodeList = {}

		for head in self.repo.heads:
			branch = head.name
			for refLogItem in head.log():
				if refLogItem.message[0:6] != "commit": continue

				node = Node()
				node.hash = refLogItem.newhexsha
				node.branch = branch
				self.nodeList[node.hash] = node

		for head in self.repo.heads:
			for commit in self.repo.iter_commits(head):
				#print(dir(commit))
				#return
				node = self.nodeList[commit.hexsha]
				node.commit = commit

		for hash in self.nodeList: 
			self.nodeList[hash].dump()


class Node:


	def dump(self):

		print(
			self.hash[0:6] + "..."
			+ " - " + self.commit.message.strip()
			+ " - #" + self.branch
			+ " - " + str(self.commit.committed_datetime)
		)


if __name__ == "__main__":
	GitFlowGraph().main()