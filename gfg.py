#!/usr/bin/env python2
import sys
import os
from git import Repo


class GitFlowGraph:


	def main(self):

		try: self.repo = Repo(sys.argv[1])
		except:
			print("specify directory contains a repository")
			os._exit(2)

		self.entries = {}

		for head in self.repo.heads:
			for entry in head.log():
				self.store(entry)

		for i in self.entries:
			entry = self.entries[i]
			print(entry.newhexsha + " - " + entry.message)


	def store(self,entry):

		if entry.newhexsha in self.entries: return
		self.entries[entry.newhexsha] = entry


if __name__ == "__main__":
	GitFlowGraph().main()