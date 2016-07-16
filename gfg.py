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

		self.commits = {}

		for head in self.repo.heads:
			shead = str(head)
			shead = "master"
			for commit in self.repo.iter_commits(shead):
				self.store(commit,shead)

		for i in self.commits:
			commit = self.commits[i]
			print(commit.hexsha[0:7] + " - " + commit.message.replace("\n",""))


	def store(self,commit,head):

		if commit.hexsha not in self.commits: 
			self.commits[commit.hexsha] = commit
		self.commits[commit.hexsha].message += " #" + head


if __name__ == "__main__":
	GitFlowGraph().main()