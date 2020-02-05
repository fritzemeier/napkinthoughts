import sys,io
from collections import OrderedDict

def parse_args(INFO):

	MENU = { \

			"OBF":"Obfuscated algorithm file", \
			"OF":"Output file (Not implemented)"

		}

	for NUM in range(1,len(sys.argv)):
		CURR = sys.argv[NUM]

		if CURR[:2] == "--":
			if CURR[2:] == "help":
				print_dict(MENU)
				sys.exit()

		KEY = CURR.split("=")[0]

		if KEY in INFO.keys():
			INFO[KEY] = CURR[(len(KEY)+1):]

	return INFO

def parse_obfs(OBFS,IFILE):
	for LINE in IFILE:
		SFILE = LINE.split(":")[0]
		LO = LINE[(len(SFILE)+1):]
		FUNC = LO.replace(" ","").split("=")[0]
		PCS = LO.replace(" ","").replace("\n","").split("=")[1].split("+")
		OBFS[FUNC] = { \
					"SFILE":SFILE, \
					"PCS":OrderedDict(), \
					"ALG": OrderedDict(), \
					"FULLSTR":""
				}

		for PC in LO.replace(" ","").replace("\n","").split("=")[1].split("+"):
			OBFS[FUNC]["PCS"][PC] = PC

	return OBFS

def begin_deobf(OBFS,FILE):
	for KEY,DATA in OBFS.items():


		CURR_FILE = open(DATA["SFILE"],"r",encoding=ENC)

		FILE[DATA["SFILE"]] = ""

		for LINE in CURR_FILE:

			FILE[DATA["SFILE"]] += LINE

			BEGIN = LINE.replace(" ","").split("=")[0]

			if BEGIN in DATA["PCS"].keys():

				TYPE = LINE.replace(" ","").split("=")[1].split("(")[0]

				if TYPE == "Mid":
					OSTR = LINE.replace(" ","").replace("\n","").replace(")","").split("(")[1].split(",")[0]
					ENTRY = int(LINE.replace(" ","").replace("\n","").replace(")","").split("(")[1].split(",")[1])
					LEN = int(LINE.replace(" ","").replace("\n","").replace(")","").split("(")[1].split(",")[2])

					DATA["ALG"][BEGIN] = { \
									"TYPE":TYPE, \
									"OSTR":OSTR, \
									"ENTRY":ENTRY, \
									"LEN":LEN, \
									"STR":""
									}
			elif BEGIN == KEY:
				TYPE = LINE.replace(" ","").split("=")[1].split("(")[0]
				if TYPE == "Array":
					CHRS = LINE.replace(" ","").replace(")","").replace("\n","").split("(")[1].split(",")
					print(CHRS)


	return OBFS,FILE

def construct_deobf(OBFS,FILE):
	for KEY,DATA in OBFS.items():

		for PC1 in DATA["ALG"].keys():

			PC2 = DATA["ALG"][PC1]["OSTR"]

			for CHUNK in FILE[DATA["SFILE"]].split("\n"):

				if PC2 in CHUNK.replace(" ","").split("=")[0]:

					if DATA["ALG"][PC1]["TYPE"] == "Mid":
						ENTRY = DATA["ALG"][PC1]["ENTRY"]
						LEN = DATA["ALG"][PC1]["LEN"]

						FOUND_STR = CHUNK.replace('"','').split("=")[1][ENTRY:(ENTRY+LEN)]
						DATA["ALG"][PC1]["STR"] = FOUND_STR

	return OBFS

def print_results(OBFS):
	for KEY,DATA in OBFS.items():

		print("      Obfuscated Variable:     "+KEY)
		print("              Source File:     "+DATA["SFILE"])
		print("     De-obfuscated String\n------------------------------------------------")

		for PC in OBFS[KEY]["PCS"].keys():

			if PC in OBFS.keys() or PC[:4] == "Chr(":
				OBFS[KEY]["FULLSTR"] += "<<"+PC+">>    "
				continue
			OBFS[KEY]["FULLSTR"] += OBFS[KEY]["ALG"][PC]["STR"]

		print(OBFS[KEY]["FULLSTR"])
		print("\n\n")

def print_dict(INFO):
	for KEY in INFO.keys():
		print("  "+KEY+" "*(10-len(KEY))+"		"+str(INFO[KEY]))

def main():

	files = {}

	cliArgs = { \

			"IF":"", \
			"OF":""

		 }

	cliArgs = parse_args(cliArgs)

	if cliArgs["OF"]:
		outFile = open(cliArgs["OF"], "w")

	if cliArgs["IF"]:
		obfFile = open(cliArgs["IF"], "r")

		obfStrs = OrderedDict()

		obfStrs = parse_obfs(obfStrs,obfFile)

		obfStrs,files = begin_deobf(obfStrs,files)\

		sys.exit()

		obfStrs = construct_deobf(obfStrs,files)

		print_results(obfStrs)

if __name__ == "__main__":
	main()
