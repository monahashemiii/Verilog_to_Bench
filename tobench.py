# -------------------------------------------------------------------------------
# Copyright 2021, Benjamin Tan <benjamin.tan@nyu.edu>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# -------------------------------------------------------------------------------
# Last modified by: Mona Hashemi <hashemi.mona@ut.ac.ir>, 2023
# DSD Lab @ University of Tehran, Iran
# CompArch Group @ National University of Singapore, Singapore
# -------------------------------------------------------------------------------
# python3 tobench.py -i INPUT_FILE -o OUTPUT_FILE
# -------------------------------------------------------------------------------

import sys
import argparse
import re
Gi = 0

def main():

    INFO = "Post-Synthesis Verilog Netlist to Bench"
    VERSION = 0.1
    USAGE = "Usage: python3 tobench.py -i INPUT_FILE -o OUTPUT_FILE"
    global Gi

    def showVersion():
        print(INFO)
        print(VERSION)
        print(USAGE)
        sys.exit()

    argparser = argparse.ArgumentParser(description="Assumes only one verilog module in file")
    argparser.add_argument("-V", "--version", action="store_true", dest="showversion", default=False, help="Show the version")
    argparser.add_argument("-i", "--input_file", action="store", dest="input_file", default="", help="Specify the name of the netlist file to process")
    argparser.add_argument("-o", "--output_file", action="store", dest="output_file", default="out.bench", help="Specify the name of the output file")
    argparser.add_argument("--for_formal_check_reg", action="store_true", dest="formality_aid", default=False, help="Try to keep reg names")

    # read arguments/options from the cmd line
    args = argparser.parse_args()

    if args.showversion:
        showVersion()

    if args.input_file == '':
        args.input_file = args[0]

    print("Reading File: " + args.input_file)
    #G = 1
    with open(args.input_file, 'r') as f:
        line = ''
        with open(args.output_file, 'w') as outfile:

            while True:
                line += f.readline()
                if "endmodule" in line: # assume that netlist file has only one module!
                    break
                elif "//" == line[:2]: # ignore lines that start with comments ... e.g., synopsys header
                    line = ''
                elif ";" in line: # once we've reached the end of a statement
                    line = ' '.join(line.split()) # get rid of multiple spaces and trailing spaces
                    line = line.replace('\n','') # get rid of newlines in the middle of an instantiation
                    outfile.write(process_cell(line, args.formality_aid))
                    line = ''

        print("Done: "+ args.output_file)

def process_cell(line, formal_help):
    global Gi
        #Gi = 1
    newline = ''

    if "input " in line:
        to_process = line.replace("input ","").replace(' ', '').replace(";",'').split(",")
        # print(to_process)
        for port in to_process:
            newline += "INPUT(" + port + ")\n"
        return newline
    elif "output " in line:
        to_process = line.replace("output ","").replace(' ', '').replace(";",'').split(",")
        # print(to_process)
        for port in to_process:
            newline += "OUTPUT(" + port + ")\n"
        return newline
    elif "module " in line:
        return "###\n"
    elif "wire " in line:
        return ""
    elif "tri " in line:
        return ""

    # newline = line.replace(' ','')
    # to_process = newline.split(",")

    ### Continue on for regular nodes

    # extract node type and name
    test = line.split(" ")
    test = test[:2]

    newline = line.replace(' ','')
    to_process = newline.split(",")

    #Gi = 1

    if "INVX1" in test[0]:
        newline = (re.search( ".Y\((.*?)\)", str(to_process)).group(1) + " = not(" + re.search( ".A\((.*?)\)", str(to_process)).group(1) + ")")
    elif "INVX2" in test[0]:
        newline = (re.search( ".Y\((.*?)\)", str(to_process)).group(1) + " = not(" + re.search( ".A\((.*?)\)", str(to_process)).group(1) + ")")
    elif "INVX4" in test[0]:
        newline = (re.search( ".Y\((.*?)\)", str(to_process)).group(1) + " = not(" + re.search( ".A\((.*?)\)", str(to_process)).group(1) + ")")
    elif "INVX8" in test[0]:
        newline = (re.search( ".Y\((.*?)\)", str(to_process)).group(1) + " = not(" + re.search( ".A\((.*?)\)", str(to_process)).group(1) + ")")

    elif "BUFX1" in test[0]:
        newline = (re.search( ".Y\((.*?)\)", str(to_process)).group(1) + " = buf(" + re.search( ".A\((.*?)\)", str(to_process)).group(1) + ")")
    elif "BUFX3" in test[0]:
        newline = (re.search( ".Y\((.*?)\)", str(to_process)).group(1) + " = buf(" + re.search( ".A\((.*?)\)", str(to_process)).group(1) + ")")

    elif "CLKBUFX1" in test[0]:
        newline = (re.search( ".Y\((.*?)\)", str(to_process)).group(1) + " = buf(" + re.search( ".A\((.*?)\)", str(to_process)).group(1) + ")")
    elif "CLKBUFX2" in test[0]:
        newline = (re.search( ".Y\((.*?)\)", str(to_process)).group(1) + " = buf(" + re.search( ".A\((.*?)\)", str(to_process)).group(1) + ")")
    elif "CLKBUFX3" in test[0]:
        newline = (re.search( ".Y\((.*?)\)", str(to_process)).group(1) + " = buf(" + re.search( ".A\((.*?)\)", str(to_process)).group(1) + ")")

    elif "NAND2X1" in test[0]:
        newline = (re.search( ".Y\((.*?)\)", str(to_process)).group(1) + " = nand(" + re.search( ".A\((.*?)\)", str(to_process)).group(1) + "," + re.search( ".B\((.*?)\)", str(to_process)).group(1) +")")
    elif "NAND2X2" in test[0]:
        newline = (re.search( ".Y\((.*?)\)", str(to_process)).group(1) + " = nand(" + re.search( ".A\((.*?)\)", str(to_process)).group(1) + "," + re.search( ".B\((.*?)\)", str(to_process)).group(1) +")")
    elif "NAND2BX1" in test[0]:
        newline = ("NAND2BX1_" + str(Gi) + " = not(" + re.search( ".AN\((.*?)\)", str(to_process)).group(1) + ")\n")
        Gi += 1
        newline += (re.search( ".Y\((.*?)\)", str(to_process)).group(1) + " = nand(" + "NAND2BX1_" + str(Gi-1) + "," + re.search( ".B\((.*?)\)", str(to_process)).group(1) +")")
    elif "NAND3X1" in test[0]:
        newline = (re.search( ".Y\((.*?)\)", str(to_process)).group(1) + " = nand(" + re.search( ".A\((.*?)\)", str(to_process)).group(1) + "," + re.search( ".B\((.*?)\)", str(to_process)).group(1) + "," + re.search( ".C\((.*?)\)", str(to_process)).group(1) +")")
    elif "NAND3BX1" in test[0]:
        newline = ("NAND3BX1_" + str(Gi) + " = not(" + re.search( ".AN\((.*?)\)", str(to_process)).group(1) + ")\n")
        Gi += 1
        newline += (re.search( ".Y\((.*?)\)", str(to_process)).group(1) + " = nand(" + "NAND3BX1_" + str(Gi-1) + "," + re.search( ".B\((.*?)\)", str(to_process)).group(1) + "," + re.search( ".C\((.*?)\)", str(to_process)).group(1) +")")
    elif "NAND4X1" in test[0]:
        newline = (re.search( ".Y\((.*?)\)", str(to_process)).group(1) + " = nand(" + re.search( ".A\((.*?)\)", str(to_process)).group(1) + "," + re.search( ".B\((.*?)\)", str(to_process)).group(1) + "," + re.search( ".C\((.*?)\)", str(to_process)).group(1) + "," + re.search( ".D\((.*?)\)", str(to_process)).group(1) +")")
    elif "NAND4BXL" in test[0]:
        newline = ("NAND4BXL_" + str(Gi) + " = not(" + re.search( ".AN\((.*?)\)", str(to_process)).group(1) + ")\n")
        Gi += 1
        newline += (re.search( ".Y\((.*?)\)", str(to_process)).group(1) + " = nand(" + "NAND4BXL_" + str(Gi-1) + "," + re.search( ".B\((.*?)\)", str(to_process)).group(1) + "," + re.search( ".C\((.*?)\)", str(to_process)).group(1) + "," + re.search( ".D\((.*?)\)", str(to_process)).group(1) +")")
    elif "NAND4BBX1" in test[0]:
        newline = ("NAND4BBX1_" + str(Gi) + " = not(" + re.search( ".AN\((.*?)\)", str(to_process)).group(1) + ")\n")
        Gi += 1
        newline = ("NAND4BBX1_" + str(Gi) + " = not(" + re.search( ".BN\((.*?)\)", str(to_process)).group(1) + ")\n")
        Gi += 1
        newline += (re.search( ".Y\((.*?)\)", str(to_process)).group(1) + " = nand(" + "NAND4BBX1_" + str(Gi-1) + "," + "NAND4BBX1_" + str(Gi-2) + "," + re.search( ".C\((.*?)\)", str(to_process)).group(1) + "," + re.search( ".D\((.*?)\)", str(to_process)).group(1) +")")

    elif "AND2X1" in test[0]:
        newline = (re.search( ".Y\((.*?)\)", str(to_process)).group(1) + " = and(" + re.search( ".A\((.*?)\)", str(to_process)).group(1) + "," + re.search( ".B\((.*?)\)", str(to_process)).group(1) +")")
    elif "AND3X1" in test[0]:
        newline = (re.search( ".Y\((.*?)\)", str(to_process)).group(1) + " = and(" + re.search( ".A\((.*?)\)", str(to_process)).group(1) + "," + re.search( ".B\((.*?)\)", str(to_process)).group(1) + "," + re.search( ".C\((.*?)\)", str(to_process)).group(1) +")")
    elif "AND4X1" in test[0]:
        newline = (re.search( ".Y\((.*?)\)", str(to_process)).group(1) + " = and(" + re.search( ".A\((.*?)\)", str(to_process)).group(1) + "," + re.search( ".B\((.*?)\)", str(to_process)).group(1) + "," + re.search( ".C\((.*?)\)", str(to_process)).group(1) + "," + re.search( ".D\((.*?)\)", str(to_process)).group(1) +")")

    elif "XNOR2X2" in test[0]:
        newline = (re.search( ".Y\((.*?)\)", str(to_process)).group(1) + " = xnor(" + re.search( ".A\((.*?)\)", str(to_process)).group(1) + "," + re.search( ".B\((.*?)\)", str(to_process)).group(1) +")")
    elif "XNOR2X1" in test[0]:
        newline = (re.search( ".Y\((.*?)\)", str(to_process)).group(1) + " = xnor(" + re.search( ".A\((.*?)\)", str(to_process)).group(1) + "," + re.search( ".B\((.*?)\)", str(to_process)).group(1) +")")
    elif "XNOR2X4" in test[0]:
        newline = (re.search( ".Y\((.*?)\)", str(to_process)).group(1) + " = xnor(" + re.search( ".A\((.*?)\)", str(to_process)).group(1) + "," + re.search( ".B\((.*?)\)", str(to_process)).group(1) +")")

    elif "XOR2X1" in test[0]:
        newline = (re.search( ".Y\((.*?)\)", str(to_process)).group(1) + " = xor(" + re.search( ".A\((.*?)\)", str(to_process)).group(1) + "," + re.search( ".B\((.*?)\)", str(to_process)).group(1) +")")
    elif "XOR2X2" in test[0]:
        newline = (re.search( ".Y\((.*?)\)", str(to_process)).group(1) + " = xor(" + re.search( ".A\((.*?)\)", str(to_process)).group(1) + "," + re.search( ".B\((.*?)\)", str(to_process)).group(1) +")")

    elif "NOR2X1" in test[0]:
        newline = (re.search( ".Y\((.*?)\)", str(to_process)).group(1) + " = nor(" + re.search( ".A\((.*?)\)", str(to_process)).group(1) + "," + re.search( ".B\((.*?)\)", str(to_process)).group(1) +")")
    elif "NOR2BX1" in test[0]:
        newline = ("NOR2BX1_" + str(Gi) + " = not(" + re.search( ".AN\((.*?)\)", str(to_process)).group(1) + ")\n")
        Gi += 1
        newline += (re.search( ".Y\((.*?)\)", str(to_process)).group(1) + " = nor(" + "NOR2BX1_" + str(Gi-1) + "," + re.search( ".B\((.*?)\)", str(to_process)).group(1) +")")
    elif "NOR3X1" in test[0]:
        newline = (re.search( ".Y\((.*?)\)", str(to_process)).group(1) + " = nor(" + re.search( ".A\((.*?)\)", str(to_process)).group(1) + "," + re.search( ".B\((.*?)\)", str(to_process)).group(1) + "," + re.search( ".C\((.*?)\)", str(to_process)).group(1) +")")
    elif "NOR3BX1" in test[0]:
        newline = ("NOR3BX1_" + str(Gi) + " = not(" + re.search( ".AN\((.*?)\)", str(to_process)).group(1) + ")\n")
        Gi += 1
        newline += (re.search( ".Y\((.*?)\)", str(to_process)).group(1) + " = nor(" + "NOR3BX1_" + str(Gi-1) + "," + re.search( ".B\((.*?)\)", str(to_process)).group(1) + "," + re.search( ".C\((.*?)\)", str(to_process)).group(1) +")")
    elif "NOR4X1" in test[0]:
        newline = (re.search( ".Y\((.*?)\)", str(to_process)).group(1) + " = nor(" + re.search( ".A\((.*?)\)", str(to_process)).group(1) + "," + re.search( ".B\((.*?)\)", str(to_process)).group(1) + "," + re.search( ".C\((.*?)\)", str(to_process)).group(1) + "," + re.search( ".D\((.*?)\)", str(to_process)).group(1) +")")
    elif "NOR4BX1" in test[0]:
        newline = ("NOR4BX1_" + str(Gi) + " = not(" + re.search( ".AN\((.*?)\)", str(to_process)).group(1) + ")\n")
        Gi += 1
        newline += (re.search( ".Y\((.*?)\)", str(to_process)).group(1) + " = nor(" + "NOR4BX1_" + str(Gi-1) + "," + re.search( ".B\((.*?)\)", str(to_process)).group(1) + "," + re.search( ".C\((.*?)\)", str(to_process)).group(1) + "," + re.search( ".D\((.*?)\)", str(to_process)).group(1) +")")

    elif "OR2X1" in test[0]:
        newline = (re.search( ".Y\((.*?)\)", str(to_process)).group(1) + " = or(" + re.search( ".A\((.*?)\)", str(to_process)).group(1) + "," + re.search( ".B\((.*?)\)", str(to_process)).group(1) +")")
    elif "OR3X1" in test[0]:
        newline = (re.search( ".Y\((.*?)\)", str(to_process)).group(1) + " = or(" + re.search( ".A\((.*?)\)", str(to_process)).group(1) + "," + re.search( ".B\((.*?)\)", str(to_process)).group(1) + "," + re.search( ".C\((.*?)\)", str(to_process)).group(1) +")")
    elif "OR3XL" in test[0]:
        newline = (re.search( ".Y\((.*?)\)", str(to_process)).group(1) + " = or(" + re.search( ".A\((.*?)\)", str(to_process)).group(1) + "," + re.search( ".B\((.*?)\)", str(to_process)).group(1) + "," + re.search( ".C\((.*?)\)", str(to_process)).group(1) +")")
    elif "OR4X1" in test[0]:
        newline = (re.search( ".Y\((.*?)\)", str(to_process)).group(1) + " = or(" + re.search( ".A\((.*?)\)", str(to_process)).group(1) + "," + re.search( ".B\((.*?)\)", str(to_process)).group(1) + "," + re.search( ".C\((.*?)\)", str(to_process)).group(1) + "," + re.search( ".D\((.*?)\)", str(to_process)).group(1) +")")

    elif "OAI21X1" in test[0]:
        newline = ("OAI21X1_" + str(Gi) + " = or(" + re.search( ".A0\((.*?)\)", str(to_process)).group(1) + "," + re.search( ".A1\((.*?)\)", str(to_process)).group(1) +")\n")
        newline += (re.search( ".Y\((.*?)\)", str(to_process)).group(1) + " = nand(" + "OAI21X1_" + str(Gi) + "," + re.search( ".B0\((.*?)\)", str(to_process)).group(1) +")")
        Gi += 1
    elif "OAI21XL" in test[0]:
        newline = ("OAI21XL_" + str(Gi) + " = or(" + re.search( ".A0\((.*?)\)", str(to_process)).group(1) + "," + re.search( ".A1\((.*?)\)", str(to_process)).group(1) +")\n")
        newline += (re.search( ".Y\((.*?)\)", str(to_process)).group(1) + " = nand(" + "OAI21XL_" + str(Gi) + "," + re.search( ".B0\((.*?)\)", str(to_process)).group(1) +")")
        Gi += 1
    elif "OAI211X1" in test[0]:
        newline = ("OAI211X1_" + str(Gi) + " = or(" + re.search( ".A0\((.*?)\)", str(to_process)).group(1) + "," + re.search( ".A1\((.*?)\)", str(to_process)).group(1) +")\n")
        newline += (re.search( ".Y\((.*?)\)", str(to_process)).group(1) + " = nand(" + "OAI211X1_" + str(Gi) + "," + re.search( ".B0\((.*?)\)", str(to_process)).group(1) + "," + re.search( ".C0\((.*?)\)", str(to_process)).group(1) +")")
        Gi += 1
    elif "OAI22X1" in test[0]:
        newline = ("OAI22X1_" + str(Gi) + " = or(" + re.search( ".A0\((.*?)\)", str(to_process)).group(1) + "," + re.search( ".A1\((.*?)\)", str(to_process)).group(1) +")\n")
        Gi += 1
        newline += ("OAI22X1_" + str(Gi) + " = or(" + re.search( ".B0\((.*?)\)", str(to_process)).group(1) + "," + re.search( ".B1\((.*?)\)", str(to_process)).group(1) +")\n")
        newline += (re.search( ".Y\((.*?)\)", str(to_process)).group(1) + " = nand(" + "OAI22X1_" + str(Gi) + "," + "OAI22X1_" + str(Gi-1)+")")
        Gi += 1
    elif "OAI221XL" in test[0]:
        newline = ("OAI221XL_" + str(Gi) + " = or(" + re.search( ".A0\((.*?)\)", str(to_process)).group(1) + "," + re.search( ".A1\((.*?)\)", str(to_process)).group(1) +")\n")
        Gi += 1
        newline += ("OAI221XL_" + str(Gi) + " = or(" + re.search( ".B0\((.*?)\)", str(to_process)).group(1) + "," + re.search( ".B1\((.*?)\)", str(to_process)).group(1) +")\n")
        newline += (re.search( ".Y\((.*?)\)", str(to_process)).group(1) + " = nand(" + "OAI221XL_" + str(Gi) + "," + "OAI221XL_" + str(Gi-1)+ "," + re.search( ".C0\((.*?)\)", str(to_process)).group(1) +")")
        Gi += 1
    elif "OAI221X1" in test[0]:
        newline = ("OAI221X1_" + str(Gi) + " = or(" + re.search( ".A0\((.*?)\)", str(to_process)).group(1) + "," + re.search( ".A1\((.*?)\)", str(to_process)).group(1) +")\n")
        Gi += 1
        newline += ("OAI221X1_" + str(Gi) + " = or(" + re.search( ".B0\((.*?)\)", str(to_process)).group(1) + "," + re.search( ".B1\((.*?)\)", str(to_process)).group(1) +")\n")
        newline += (re.search( ".Y\((.*?)\)", str(to_process)).group(1) + " = nand(" + "OAI221X1_" + str(Gi) + "," + "OAI221X1_" + str(Gi-1)+ "," + re.search( ".C0\((.*?)\)", str(to_process)).group(1) +")")
        Gi += 1
    elif "OAI2BB1X1" in test[0]:
        newline = ("OAI2BB1X1_" + str(Gi) + " = not(" + re.search( ".A0N\((.*?)\)", str(to_process)).group(1) + ")\n")
        Gi += 1
        newline += ("OAI2BB1X1_" + str(Gi) + " = not(" + re.search( ".A1N\((.*?)\)", str(to_process)).group(1) + ")\n")
        Gi += 1
        newline += ("OAI2BB1X1_" + str(Gi) + " = or(" + "OAI2BB1X1_" + str(Gi-1)+ "," + "OAI2BB1X1_" + str(Gi-2) +")\n")
        newline += (re.search( ".Y\((.*?)\)", str(to_process)).group(1) + " = nand(" + "OAI2BB1X1_" + str(Gi) + "," + re.search( ".B0\((.*?)\)", str(to_process)).group(1) +")")
        Gi += 1
    elif "OAI2BB2X1" in test[0]:
        newline = ("OAI2BB2X1_" + str(Gi) + " = not(" + re.search( ".A0N\((.*?)\)", str(to_process)).group(1) + ")\n")
        Gi += 1
        newline += ("OAI2BB2X1_" + str(Gi) + " = not(" + re.search( ".A1N\((.*?)\)", str(to_process)).group(1) + ")\n")
        Gi += 1
        newline += ("OAI2BB2X1_" + str(Gi) + " = or(" + "OAI2BB2X1_" + str(Gi-1)+ "," + "OAI2BB2X1_" + str(Gi-2) +")\n")
        Gi += 1
        newline += ("OAI2BB2X1_" + str(Gi) + " = or(" + re.search( ".B0\((.*?)\)", str(to_process)).group(1) + "," + re.search( ".B1\((.*?)\)", str(to_process)).group(1) +")\n")
        newline += (re.search( ".Y\((.*?)\)", str(to_process)).group(1) + " = nand(" + "OAI2BB2X1_" + str(Gi) + "," + "OAI2BB2X1_" + str(Gi-1)+")")
        Gi += 1
    elif "OAI31X1" in test[0]:
        newline = ("OAI31X1_" + str(Gi) + " = or(" + re.search( ".A0\((.*?)\)", str(to_process)).group(1) + "," + re.search( ".A1\((.*?)\)", str(to_process)).group(1)  + "," + re.search( ".A2\((.*?)\)", str(to_process)).group(1)+")\n")
        Gi += 1
        newline += (re.search( ".Y\((.*?)\)", str(to_process)).group(1) + " = nand(" + re.search( ".B0\((.*?)\)", str(to_process)).group(1) + "," + "OAI31X1_" + str(Gi-1) +")")
        Gi += 1
    elif "OAI32X1" in test[0]:
        newline = ("OAI32X1_" + str(Gi) + " = or(" + re.search( ".A0\((.*?)\)", str(to_process)).group(1) + "," + re.search( ".A1\((.*?)\)", str(to_process)).group(1)  + "," + re.search( ".A2\((.*?)\)", str(to_process)).group(1)+")\n")
        Gi += 1
        newline += ("OAI32X1_" + str(Gi) + " = or(" + re.search( ".B0\((.*?)\)", str(to_process)).group(1) + "," + re.search( ".B1\((.*?)\)", str(to_process)).group(1) +")\n")
        newline += (re.search( ".Y\((.*?)\)", str(to_process)).group(1) + " = nand(" + "OAI32X1_" + str(Gi) + "," + "OAI32X1_" + str(Gi-1) +")")
        Gi += 1
    elif "OAI33X1" in test[0]:
        newline = ("OAI33X1_" + str(Gi) + " = or(" + re.search( ".A0\((.*?)\)", str(to_process)).group(1) + "," + re.search( ".A1\((.*?)\)", str(to_process)).group(1)  + "," + re.search( ".A2\((.*?)\)", str(to_process)).group(1)+")\n")
        Gi += 1
        newline += ("OAI33X1_" + str(Gi) + " = or(" + re.search( ".B0\((.*?)\)", str(to_process)).group(1) + "," + re.search( ".B1\((.*?)\)", str(to_process)).group(1) + "," + re.search( ".B2\((.*?)\)", str(to_process)).group(1)+")\n")
        newline += (re.search( ".Y\((.*?)\)", str(to_process)).group(1) + " = nand(" + "OAI33X1_" + str(Gi) + "," + "OAI33X1_" + str(Gi-1) +")")
        Gi += 1

    elif "AOI21X1" in test[0]:
        newline = ("AOI21X1_" + str(Gi) + " = and(" + re.search( ".A0\((.*?)\)", str(to_process)).group(1) + "," + re.search( ".A1\((.*?)\)", str(to_process)).group(1) +")\n")
        newline += (re.search( ".Y\((.*?)\)", str(to_process)).group(1) + " = nor(" + "AOI21X1_" + str(Gi) + "," + re.search( ".B0\((.*?)\)", str(to_process)).group(1) +")")
        Gi += 1
    elif "AOI211X1" in test[0]:
        newline = ("AOI211X1_" + str(Gi) + " = and(" + re.search( ".A0\((.*?)\)", str(to_process)).group(1) + "," + re.search( ".A1\((.*?)\)", str(to_process)).group(1) +")\n")
        newline += (re.search( ".Y\((.*?)\)", str(to_process)).group(1) + " = nor(" + "AOI211X1_" + str(Gi) + "," + re.search( ".B0\((.*?)\)", str(to_process)).group(1) + "," + re.search( ".C0\((.*?)\)", str(to_process)).group(1)+")")
        Gi += 1
    elif "AOI22X1" in test[0]:
        newline = ("AOI22X1_" + str(Gi) + " = and(" + re.search( ".A0\((.*?)\)", str(to_process)).group(1) + "," + re.search( ".A1\((.*?)\)", str(to_process)).group(1) +")\n")
        Gi += 1
        newline += ("AOI22X1_" + str(Gi) + " = and(" + re.search( ".B0\((.*?)\)", str(to_process)).group(1) + "," + re.search( ".B1\((.*?)\)", str(to_process)).group(1) +")\n")
        newline += (re.search( ".Y\((.*?)\)", str(to_process)).group(1) + " = nor(" + "AOI22X1_" + str(Gi) +  "," + "AOI22X1_" + str(Gi-1) + ")")
        Gi += 1
    elif "AOI221X1" in test[0]:
        newline = ("AOI221X1_" + str(Gi) + " = and(" + re.search( ".A0\((.*?)\)", str(to_process)).group(1) + "," + re.search( ".A1\((.*?)\)", str(to_process)).group(1) +")\n")
        Gi += 1
        newline += ("AOI221X1_" + str(Gi) + " = and(" + re.search( ".B0\((.*?)\)", str(to_process)).group(1) + "," + re.search( ".B1\((.*?)\)", str(to_process)).group(1) +")\n")
        newline += (re.search( ".Y\((.*?)\)", str(to_process)).group(1) + " = nor(" + "AOI221X1_" + str(Gi) +  "," + "AOI221X1_" + str(Gi-1) + "," + re.search( ".C0\((.*?)\)", str(to_process)).group(1)+")")
        Gi += 1
    elif "AOI222X1" in test[0]:
        newline = ("AOI222X1_" + str(Gi) + " = and(" + re.search( ".A0\((.*?)\)", str(to_process)).group(1) + "," + re.search( ".A1\((.*?)\)", str(to_process)).group(1) +")\n")
        Gi += 1
        newline += ("AOI222X1_" + str(Gi) + " = and(" + re.search( ".B0\((.*?)\)", str(to_process)).group(1) + "," + re.search( ".B1\((.*?)\)", str(to_process)).group(1) +")\n")
        Gi += 1
        newline += ("AOI222X1_" + str(Gi) + " = and(" + re.search( ".C0\((.*?)\)", str(to_process)).group(1) + "," + re.search( ".C1\((.*?)\)", str(to_process)).group(1) +")\n")
        newline += (re.search( ".Y\((.*?)\)", str(to_process)).group(1) + " = nor(" + "AOI222X1_" + str(Gi) +  "," + "AOI222X1_" + str(Gi-1) +  "," + "AOI222X1_" + str(Gi-2) +")")
        Gi += 1
    elif "AOI2BB1X1" in test[0]:
        newline = ("AOI2BB1X1_" + str(Gi) + " = not(" + re.search( ".A0N\((.*?)\)", str(to_process)).group(1) + ")\n")
        Gi += 1
        newline += ("AOI2BB1X1_" + str(Gi) + " = not(" + re.search( ".A1N\((.*?)\)", str(to_process)).group(1) + ")\n")
        Gi += 1
        newline += ("AOI2BB1X1_" + str(Gi) + " = and(" + "AOI2BB1X1_" + str(Gi-1)+ "," + "AOI2BB1X1_" + str(Gi-2) +")\n")
        newline += (re.search( ".Y\((.*?)\)", str(to_process)).group(1) + " = nor(" + "AOI2BB1X1_" + str(Gi) + "," + re.search( ".B0\((.*?)\)", str(to_process)).group(1) +")")
        Gi += 1
    elif "AOI2BB2X1" in test[0]:
        newline = ("AOI2BB2X1_" + str(Gi) + " = not(" + re.search( ".A0N\((.*?)\)", str(to_process)).group(1) + ")\n")
        Gi += 1
        newline += ("AOI2BB2X1_" + str(Gi) + " = not(" + re.search( ".A1N\((.*?)\)", str(to_process)).group(1) + ")\n")
        Gi += 1
        newline += ("AOI2BB2X1_" + str(Gi) + " = and(" + "AOI2BB2X1_" + str(Gi-1)+ "," + "AOI2BB2X1_" + str(Gi-2) +")\n")
        Gi += 1
        newline += ("AOI2BB2X1_" + str(Gi) + " = and(" + re.search( ".B0\((.*?)\)", str(to_process)).group(1) + "," + re.search( ".B1\((.*?)\)", str(to_process)).group(1) +")\n")
        newline += (re.search( ".Y\((.*?)\)", str(to_process)).group(1) + " = nor(" + "AOI2BB2X1_" + str(Gi) + "," + "AOI2BB2X1_" + str(Gi-1) +")")
        Gi += 1
    elif "AOI31X1" in test[0]:
        newline = ("AOI31X1_" + str(Gi) + " = and(" + re.search( ".A0\((.*?)\)", str(to_process)).group(1) + "," + re.search( ".A1\((.*?)\)", str(to_process)).group(1)+ "," + re.search( ".A2\((.*?)\)", str(to_process)).group(1) +")\n")
        newline += (re.search( ".Y\((.*?)\)", str(to_process)).group(1) + " = nor(" + "AOI31X1_" + str(Gi) + "," + re.search( ".B0\((.*?)\)", str(to_process)).group(1) +")")
        Gi += 1
    elif "AOI33X1" in test[0]:
        newline = ("AOI33X1_" + str(Gi) + " = and(" + re.search( ".A0\((.*?)\)", str(to_process)).group(1) + "," + re.search( ".A1\((.*?)\)", str(to_process)).group(1)+ "," + re.search( ".A2\((.*?)\)", str(to_process)).group(1) +")\n")
        Gi += 1
        newline += ("AOI33X1_" + str(Gi) + " = and(" + re.search( ".B0\((.*?)\)", str(to_process)).group(1) + "," + re.search( ".B1\((.*?)\)", str(to_process)).group(1)+ "," + re.search( ".B2\((.*?)\)", str(to_process)).group(1) +")\n")
        newline += (re.search( ".Y\((.*?)\)", str(to_process)).group(1) + " = nor(" + "AOI33X1_" + str(Gi) + "," + "AOI33X1_" + str(Gi-1) +")")
        Gi += 1
    elif "AOI32X1" in test[0]:
        newline = ("AOI32X1_" + str(Gi) + " = and(" + re.search( ".A0\((.*?)\)", str(to_process)).group(1) + "," + re.search( ".A1\((.*?)\)", str(to_process)).group(1)+ "," + re.search( ".A2\((.*?)\)", str(to_process)).group(1) +")\n")
        Gi += 1
        newline += ("AOI32X1_" + str(Gi) + " = and(" + re.search( ".B0\((.*?)\)", str(to_process)).group(1) + "," + re.search( ".B1\((.*?)\)", str(to_process)).group(1) +")\n")
        newline += (re.search( ".Y\((.*?)\)", str(to_process)).group(1) + " = nor(" + "AOI32X1_" + str(Gi) + "," + "AOI32X1_" + str(Gi-1) +")")
        Gi += 1

    elif "MX2X1" in test[0]:
        newline = ("MX2X1_" + str(Gi) + " = and(" + re.search( ".A\((.*?)\)", str(to_process)).group(1) + "," + re.search( ".B\((.*?)\)", str(to_process)).group(1) +")\n")
        Gi += 1
        newline += ("MX2X1_" + str(Gi) + " = and(" + re.search( ".S0\((.*?)\)", str(to_process)).group(1) + "," + re.search( ".B\((.*?)\)", str(to_process)).group(1) +")\n")
        Gi += 1
        newline += ("MX2X1_" + str(Gi) + " = not(" + re.search( ".S0\((.*?)\)", str(to_process)).group(1)+")\n")
        Gi += 1
        newline += ("MX2X1_" + str(Gi) + " = or(" + "MX2X1_" + str(Gi-1) + "," + re.search( ".A\((.*?)\)", str(to_process)).group(1) +")\n")
        newline += (re.search( ".Y\((.*?)\)", str(to_process)).group(1) + " = or(" + "MX2X1_" + str(Gi) +  "," + "MX2X1_" + str(Gi-2) +  "," + "MX2X1_" + str(Gi-3) +")")
        Gi += 1
    elif "MXI2X1" in test[0]:
        newline = ("MXI2X1_" + str(Gi) + " = and(" + re.search( ".A\((.*?)\)", str(to_process)).group(1) + "," + re.search( ".B\((.*?)\)", str(to_process)).group(1) +")\n")
        Gi += 1
        newline += ("MXI2X1_" + str(Gi) + " = and(" + re.search( ".S0\((.*?)\)", str(to_process)).group(1) + "," + re.search( ".B\((.*?)\)", str(to_process)).group(1) +")\n")
        Gi += 1
        newline += ("MXI2X1_" + str(Gi) + " = not(" + re.search( ".S0\((.*?)\)", str(to_process)).group(1)+")\n")
        Gi += 1
        newline += ("MXI2X1_" + str(Gi) + " = nor(" + "MXI2X1_" + str(Gi-1) + "," + re.search( ".A\((.*?)\)", str(to_process)).group(1) +")\n")
        newline += (re.search( ".Y\((.*?)\)", str(to_process)).group(1) + " = or(" + "MXI2X1_" + str(Gi) +  "," + "MXI2X1_" + str(Gi-2) +  "," + "MXI2X1_" + str(Gi-3) +")")
        Gi += 1

    elif "DFF" in test[0]:
        if formal_help:
            newline = test[1] + " = DFF(" + re.search( ".D\((.*?)\)", str(to_process)).group(1)+ ")\n"
            newline += re.search( ".Q\((.*?)\)", str(to_process)).group(1) + " = buf(" + test[1] + ")"
        else:
            newline = (re.search( ".Q\((.*?)\)", str(to_process)).group(1) + " = DFF(" + re.search( ".D\((.*?)\)", str(to_process)).group(1)+ ")")

    else:
        newline = line
    return newline + '\n'

if __name__ == "__main__":
    main()
    