#!/usr/bin/env python2
import sys
import os
import datetime
import SocketServer
import SimpleHTTPServer 
from git import *


class Node:

	def __init__(self):		
		self.last = False
		self.parent1 = ""
		self.parent2 = ""
		self.tag = ""
		self.bfirst = False
		self.blast = False
		self.maxParallel = 0
		self.column = -1


	def dump(self):

		if self.tag != "": tagFmt = " +" + self.tag
		else: tagFmt = ""

		if self.bfirst: bf = "{"
		else: bf = ""
		if self.blast: bl = "}"
		else: bl = ""

		print(
			self.hash[0:6]
			#+ " \"" + self.message + "\""
			+ " #" + self.branch
			+ bf + bl
			+ tagFmt
			#+ " @" + self.author
			+ " " + self.stamp
			+ " [" + self.btype + ":" + str(self.column) + "]"
		)


class GitFlowGraph:


	def procArgs(self):

		try: 
			self.repoName = sys.argv[1]
			self.repo = Repo(self.repoName)
		except NameError:
			print("requires gitpython module")
			os._exit(3)
		except IndexError:
			print("specify directory contains a repository")
			os._exit(2)			
		except:
			print("not a valid repository")
			os._exit(2)



	def dump(self):
		for node in self.decSortedNodeList:
			node.dump()
		print("max. parallel feat: " + str(self.maxParallel) + " (")



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
				node.hash = str(refLogItem.newhexsha)
				node.parent1 = str(refLogItem.oldhexsha)
				if node.parent1.replace("0","") == "": node.parent1 = ""
				node.author = str(refLogItem.actor)
				node.message = str(refLogItem.message).strip()
				node.branch = str(branch)

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
					node.branch = str(branch)

				node.hash = str(commit.hexsha)
				if len(commit.parents) > 0: node.parent1 = str(commit.parents[0])
				if len(commit.parents) > 1: node.parent2 = str(commit.parents[1])
				node.author = str(commit.author)
				node.message = str(commit.message).strip()

				plus = str(commit.committed_datetime).index("+")
				node.stamp = str(commit.committed_datetime)[0:plus]


	def collectTags(self):

		for tag in self.repo.tags:
			self.nodeList[str(tag.commit)].tag = tag.name


	def sortNodes(self):

		self.decSortedNodeList = []
		for key in (
			sorted(
				self.nodeList.keys()
				,key = lambda h: self.nodeList[h].stamp
				,reverse = True
			)
		):
			self.decSortedNodeList.append( self.nodeList[key] )

		self.incSortedNodeList = []
		for key in (
			sorted(
				self.nodeList.keys()
				,key = lambda h: self.nodeList[h].stamp
				,reverse = False
			)
		):
			self.incSortedNodeList.append( self.nodeList[key] )


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


	def calcFeatBranchBorders(self):

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


	def calcFeatParallels(self):

		p = 0
		self.maxParallel = 0
		for node in self.decSortedNodeList:
			if node.btype != "feature": continue
			if node.blast: p += 1
			if p > self.maxParallel: self.maxParallel = p
			if node.bfirst: p -= 1


	def calcFeatColumns(self):

		slotAllocArray = [False] * self.maxParallel
		branchColumns = {}
		column = 0

		for node in self.decSortedNodeList:
			if node.btype != "feature": 
				node.column += self.maxParallel
				continue

			if node.blast:
				pos = column
				for i in range(0,self.maxParallel):
					if slotAllocArray[pos]:
						pos += 1
						if pos == self.maxParallel: pos = 0
						continue
					else:
						slotAllocArray[pos] = True
						break
				branchColumns[node.branch] = pos

			pos = branchColumns[node.branch]
			node.column = pos

			if node.bfirst:
				slotAllocArray[pos] = False


	def removeEmptyColumns(self):

		cols = 5 + self.maxParallel

		columnUsage = [False] * cols
		for i in self.nodeList:
			node = self.nodeList[i]
			columnUsage[node.column] = True

		columnUsage[5] = False

		columnShift = [0] * cols
		shift = 0
		for i in range(0,cols):
			columnShift[i] = shift
			if columnUsage[i]: continue
			columnShift[i] = -1
			shift += 1

		for i in self.nodeList:
			node = self.nodeList[i]
			node.column -= columnShift[node.column]


	def calcColumns(self):

		self.calcFeatBranchBorders()
		self.calcFeatParallels()
		self.calcFeatColumns()
		self.removeEmptyColumns()


	def renderStr(self,s):
		self.renderFile.write(s)


	def renderQuoted(self,s):
		self.renderStr("\"")
		self.renderStr(s)
		self.renderStr("\"")


	def renderLf(self):
		self.renderStr("\n")


	def renderIndent(self):
		self.renderStr("  " * self.indentation)


	def renderProperty(self,prop,value,isLast = False):

		if value == "": return

		if type(value) == "bool":
			if value: value = "true"
			else: value = "false"

		self.renderIndent()
		self.renderQuoted(str(prop))
		self.renderStr(": ")
		if type(value) == str:
			self.renderQuoted(value)
		else:
			self.renderStr(str(value))
		if not isLast: self.renderStr(",")
		self.renderLf()


	def renderMeta(self):

		dirName = self.repoName
		if dirName.endswith("/"):
			dirName = dirName[0 : len(dirName) - 1]
		repoName = os.path.basename(dirName)
		self.renderProperty("repo",repoName)

		self.renderProperty("columns",4 + self.maxParallel)
		self.renderProperty("rows",len(self.nodeList),True)


	def renderNode(self,node):

		self.renderProperty("hash",node.hash)
		self.renderProperty("parent1",node.parent1)
		self.renderProperty("parent2",node.parent2)
		self.renderProperty("column",node.column)
		self.renderProperty("stamp",node.stamp)
		self.renderProperty("message",node.message)
		self.renderProperty("author",node.author)
		self.renderProperty("tag",node.tag)
		self.renderProperty("branch",node.branch)
		self.renderProperty("btype",node.btype,True)


	def renderList(self):

		for node in self.decSortedNodeList:
			node.last = True
			break

		for node in self.incSortedNodeList:
			self.renderIndent()
			self.renderStr("{")
			self.renderLf()
			self.indentation += 1

			self.renderNode(node)

			self.indentation -= 1
			self.renderIndent()
			self.renderStr("}")
			if not node. last: self.renderStr(",")
			self.renderLf()
		

	def renderResult(self,fd):

		self.renderFile = fd
		
		self.indentation = 0
		
		self.renderIndent()
		self.renderStr("{")
		self.renderLf()
		self.indentation += 1

		self.renderIndent()
		self.renderQuoted("meta")
		self.renderStr(": {")
		self.renderLf()
		self.indentation += 1

		self.renderMeta()

		self.indentation -= 1
		self.renderIndent()
		self.renderStr("},")
		self.renderLf()

		self.renderIndent()
		self.renderQuoted("list")
		self.renderStr(": [")
		self.renderLf()
		self.indentation += 1

		self.renderList()

		self.indentation -= 1
		self.renderIndent()
		self.renderStr("]")
		self.renderLf()

		self.indentation -= 1
		self.renderIndent()
		self.renderStr("}")
		self.renderLf();


	def perform(self):

		self.collectNodes()
		self.collectTags()
		self.sortNodes()
		self.fillBranchTypes()
		self.calcColumns()


	def runWebServer(self):

		fail = True
		for port in range(9312,9412):
			try: 
				server = WebServer(("0.0.0.0",port),WebProc)
				fail = False
				break
			except: 
				pass
		if fail:
			print("can not start webserver")
			os._exit(2)

		url = "http://localhost:" + str(port) + "/"
		print("click this: " + url)
		server.allow_reuse_address = True
		server.app = self

		try:
			server.serve_forever()
		except KeyboardInterrupt:
			print(" - interrupted")
			server.shutdown()
			os._exit(0)


	def main(self):
		
		self.procArgs()

		try:
			dumpMode = False
			if sys.argv[2] == "dump": dumpMode = True
		except: pass
		if dumpMode:
			self.perform()
			self.dump()
			return

		self.runWebServer()


class WebServer(SocketServer.ThreadingTCPServer):

	allow_reuse_address = True


class WebProc(SimpleHTTPServer.SimpleHTTPRequestHandler):

	def __init__(self,req,clientAddress,server):
		SimpleHTTPServer.SimpleHTTPRequestHandler.__init__(self,req,clientAddress,server)
		self.server = server


	def log_message(self,format,*args):
		return


	def do_GET(self):

		if self.path.endswith("fetch"):
			self.send_response(200,"OK")
			self.send_header("Content-type","application/json")
			self.end_headers()
			self.server.app.perform()
			self.server.app.renderResult(self.wfile)

		else:
			if self.path == "/": self.path = "/frontend"
			SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)


if __name__ == "__main__":
	GitFlowGraph().main()
