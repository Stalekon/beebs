import gcc

debug = False
verbose = False
#verbose = True
other_stats = True

statements_pool = []
src_file = ''

def printd(arg,test):
	if (test): print arg

class ShowGimple(gcc.GimplePass):
	def execute(self, fun):
		if fun and fun.cfg:
			global src_file
			src_file = fun.start.file.split("/")[-1].split(".")[0]
			#printd("CONTROL FLOW GRAPH",debug)
			blocks = fun.cfg.basic_blocks

			for bb in blocks:
				#printd("BLOCK: " + str(bb.index),debug)

				gimples = bb.gimple

				for gimp in gimples:
					printd("GIMPY: " + str(gimp),debug)

					try:
						stmt = " " + gimp.exprcode.__name__
					except:
						stmt = ""
						printd("no stmt", debug)

					try:
						stmt_type = " " + gimp.exprcode.__base__.__name__
					except:
						stmt_type = ""
						printd("no stmt_type", debug)

					try:
						superclass = gimp.__class__.__name__
					except:
						superclass = ""
						printd("superclass", debug)

					categ_str = superclass + stmt_type + stmt
					printd(categ_str, debug)

					for existing_stmt in statements_pool:
						if (categ_str == existing_stmt[0]):
							existing_stmt[1]+=1
							break
					else:
						new_stmt = [categ_str, 1]
						statements_pool.append(new_stmt)

def printout():

	statements_pool.sort()

	top_string = " Result from Gimple Tree Analysis "
	ts_len = (52-len(top_string))/2

	out = open(src_file + ".gimpdump",'w')

	out.write("#"*ts_len + top_string + "#"*ts_len + "\n")

	out.write("/"+50*"="+"\\" + "\n")

	for stmt in statements_pool:
		out.write("> " + stmt[0] + ": " + str(stmt[1]) + "\n")

	out.write("\\"+50*"="+"/" + "\n")
	out.close

ps = ShowGimple(name='show-gimple')
ps.register_after('ssa')

gcc.register_callback(gcc.PLUGIN_FINISH,printout)