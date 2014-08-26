import gcc
import psutil

debug = False
verbose = False
#verbose = True

#UNUSED, BENCHMARKS WERE SPLIT BACK AGAIN
#This retrieves a list with the names of the benchmarks being compiled,
#it assumes that there is a gcc arguement such as "TEST_bench1 bench2 .. benchN"
def get_benchmark_names():
	pid = os.getpid()
	p = psutil.Process(pid)
	start_string = "TEST_"
	for arg in p.cmdline():
		if arg.startswith(start_string):
			out = arg[len(start_string):].split(' ')
			return out

#A debugging print
def printd(arg,test):
	if (test): print arg

#Here I save the different types of statements and their count
#as lists
#['statment_string', count]
statements_pool = []

#Here I keep the count of basic block with the following number of
#outgoing edges
#['number of outgoing edges', count_of_blocks]
bb_edge_counts = [['0', 0],
				  ['1', 0],
				  ['2', 0],
				  ["more than 2 ", 0]]

#Here I store the numbers of basic blocks with same sizes
#[count_of_statements, count_of_blocks]
bb_of_diff_sizes = []

#This provides the name of the current source file being compiled
src_file = gcc.get_dump_base_name().split(".")[0]

#The gcc pass retrieving the data
class ShowGimple(gcc.GimplePass):
	def execute(self, fun):
		if fun and fun.cfg:
			#printd("CONTROL FLOW GRAPH",debug)
			blocks = fun.cfg.basic_blocks

			for bb in blocks:
				#printd("BLOCK: " + str(bb.index),debug)

				edge_count = len(bb.succs)

				for ec in bb_edge_counts[:-1]:
					if str(edge_count) == ec[0]:
						ec[1] += 1
						break
				else:
					bb_edge_counts[-1][1] += 1

				gimples = bb.gimple

				bb_size = len(gimples)

				for bbs in bb_of_diff_sizes:
					if bb_size == bbs[0]:
						bbs[1] += 1
						break
				else:
					new_size = [bb_size, 1]
					bb_of_diff_sizes.append(new_size)

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

					#This is the string of the statement
					#It consists of gimple statement type,
					#type of main expression and subtype of main expression
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
	bb_of_diff_sizes.sort()

	top_string = " Result from Gimple Tree Analysis "
	ts_len = (52-len(top_string))/2

	with open(src_file + ".gimpdump",'w') as out:

		out.write("#"*ts_len + top_string + "#"*ts_len + "\n")
		out.write("/"+50*"="+"\\" + "\n")

		for stmt in statements_pool:
			out.write("> " + stmt[0] + ": " + str(stmt[1]) + "\n")

		for ec in bb_edge_counts:
			out.write("* Basic blocks with this many edges: " + ec[0] + ";" +
				" Count: " + str(ec[1]) + "\n")

		for bbs in bb_of_diff_sizes:
			out.write("+ Basic blocks with this many statments: " +
				str(bbs[0]) + ";" +
				" Count: " + str(bbs[1]) + "\n")

		out.write("\\"+50*"="+"/" + "\n")


ps = ShowGimple(name='gimple-analysis')
ps.register_after('ssa')

gcc.register_callback(gcc.PLUGIN_FINISH,printout)