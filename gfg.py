#!/usr/bin/env python2
import sys
import os
import datetime
from git import *


class GitFlowGraph:


	def procArgs(self):

		try: self.repo = Repo(sys.argv[1])
		except NameError:
			print("requires gitpython module")
			os._exit(3)
		except IndexError:
			print("specify directory contains a repository")
			os._exit(2)			
		except:
			print("not a valid repository")
			os._exit(2)


	def collectNodes(self):

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
				node.bfirst = False
				node.blast = False
				node.author = str(refLogItem.actor)
				node.tag = ""
				node.message = refLogItem.message.strip()
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
					node.branch = branch

				node.bfirst = False
				node.blast = False
				node.hash = commit.hexsha
				node.author = str(commit.author)
				node.tag = None
				node.message = commit.message.strip()
				plus = str(commit.committed_datetime).index("+")
				node.stamp = str(commit.committed_datetime)[0:plus]


	def collectTags(self):

		for tag in self.repo.tags:
			self.nodeList[str(tag.commit)].tag = tag.name


	def sortNodes(self):

		self.sortedNodeList = []

		for key in (
			sorted(
				self.nodeList.keys()
				,key = lambda h: self.nodeList[h].stamp
				,reverse = True
			)
		):
			self.sortedNodeList.append( self.nodeList[key] )


	def fillBranchTypes(self):

		for i in self.nodeList:
			node = self.nodeList[i]

			if node.branch.startswith("devel"): 
				node.btype = "develop"
				node.column = 1
			elif node.branch.startswith("release-"): 
				node.btype = "release"
				node.column = 2
			elif node.branch.startswith("hotfix-"): 
				node.btype = "hotfix"
				node.column = 3
			elif node.branch.startswith("master"): 
				node.btype = "master"
				node.column = 4
			else:
				node.btype = "feature"
				node.column = 0


	def calcColumns(self):

		self.featureBranchList = {}

		for i in self.nodeList:
			node = self.nodeList[i]
			if node.btype != "feature": continue

			branch = node.branch
			try: 
				b = self.featureBranchList[branch]
			except:
				b = [node.stamp,node.stamp,node.hash,node.hash]
				self.featureBranchList[branch] = b
			if node.stamp < b[0]: 
				b[0] = node.stamp
				b[2] = node.hash
			if node.stamp > b[1]: 
				b[1] = node.stamp	
				b[3] = node.hash

		for branch in self.featureBranchList:
			b = self.featureBranchList[branch]
			
			first = self.nodeList[ b[2] ];
			first.bfirst = True
			last = self.nodeList[ b[3] ];
			last.blast = True

		#print(self.featureBranchList)


	def main(self):
		
		self.procArgs()
		self.collectNodes()
		self.collectTags()
		self.sortNodes()
		self.fillBranchTypes()
		self.calcColumns()

		for node in self.sortedNodeList:
			node.dump()


class Node:


	def dump(self):

		if self.tag is not None: tagFmt = " - +" + self.tag
		else: tagFmt = ""

		if self.bfirst: bf = "{"
		else: bf = ""
		if self.blast: bl = "}"
		else: bl = ""

		print(
			self.hash[0:6]
			+ " \"" + self.message + "\""
			+ " #" + self.branch
			+ bf + bl
			+ tagFmt
			+ " @" + self.author
			+ " " + self.stamp
			+ " [" + self.btype + ":" + str(self.column) + "]"
		)


if __name__ == "__main__":
	GitFlowGraph().main()