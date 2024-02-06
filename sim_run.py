# -*- coding: utf-8 -*-
"""
Simulation for NS3-AliHPCC

"""

import os
import sys
import json
from sim_func import ResPack

g_jsRoot = None
g_curDir = None
g_isOutExcel = True


def forOutputTestScript(targetFile, outFile):
    with open(targetFile, "r") as infile:
        text = infile.read()
        with open(outFile, "w") as outfile:
            outfile.write(text)


def refixPath(curPath, strPath):
    curPath = curPath.strip()
    strPath = strPath.strip()
    curPath = curPath.replace("\\", "/")
    strPath = strPath.replace("\\", "/")
    if curPath[-1] != '/':
        curPath += "/"
    if strPath[0] == '/':
        strPath = strPath[1:]
    return curPath+strPath


def initMainConfig():
    global g_jsRoot
    global g_curDir
    try:
        with open(g_curDir + "/" + "sim-main.conf", "r") as file:
            g_jsRoot = json.load(file)
            if g_jsRoot == None:
                return False
            return True
    except json.JSONDecodeError as e:
        print("main.conf文件内容格式错误:", e)
        return False
    except FileNotFoundError:
        print("main.conf文件不存在")
        return False


def getConfigPath(modeName):
    global g_jsRoot
    global g_curDir
    confPath = g_jsRoot["flow"][modeName]["conf_path"]
    jsConfName = g_jsRoot["common"]["conf_name"]
    tmpPath = refixPath(g_curDir, confPath)
    #os.makedirs(tmpPath, exist_ok=True)
    if not os.path.exists(tmpPath):
        os.makedirs(tmpPath)
    tmpPath = refixPath(confPath, jsConfName["topology_file"])
    topology_path = refixPath(g_curDir, tmpPath)
    tmpPath = refixPath(confPath, jsConfName["flow_file"])
    flow_path = refixPath(g_curDir, tmpPath)
    tmpPath = refixPath(confPath, jsConfName["trace_file"])
    trace_path = refixPath(g_curDir, tmpPath)
    tmpPath = refixPath(confPath, jsConfName["trace_output_file"])
    trace_output_path = refixPath(g_curDir, tmpPath)
    tmpPath = refixPath(confPath, jsConfName["fct_output_file"])
    fct_output_path = refixPath(g_curDir, tmpPath)
    tmpPath = refixPath(confPath, jsConfName["pfc_output_file"])
    pfc_output_path = refixPath(g_curDir, tmpPath)
    tmpPath = refixPath(confPath, jsConfName["qlen_mon_file"])
    qlen_mon_path = refixPath(g_curDir, tmpPath)
    return True, topology_path, flow_path, trace_path, trace_output_path, fct_output_path, pfc_output_path, qlen_mon_path


def genBandWidth(modeName, bandWidth):
    kmaxStr = "1"
    kminStr = kmaxStr
    pmaxStr = kmaxStr
    vKminWidth = bandWidth*1000000000
    vKmaxRate = 400*bandWidth/25
    vKminRate = 100*bandWidth/25
    kmaxStr = kmaxStr + " " + str(int(vKminWidth)) + " " + str(int(vKmaxRate))
    kminStr = kminStr + " " + str(int(vKminWidth)) + " " + str(int(vKminRate))
    pmaxStr = pmaxStr + " " + str(int(vKminWidth)) + " 0.2"
    return kmaxStr, kminStr, pmaxStr


def genBandWidthArray(modeName, jsBandWidth):
    bandWidth = jsBandWidth
    bandLen = len(bandWidth)
    kmaxStr = str(bandLen)
    kminStr = kmaxStr
    pmaxStr = kmaxStr
    # ------------------------------------------------------------------------------------
    # print("2 %d %d %d %d"%(bw*1000000000, 400*bw/25, bw*4*1000000000, 400*bw*4/25))
    # print("2 %d %d %d %d"%(bw*1000000000, 100*bw/25, bw*4*1000000000, 100*bw*4/25))
    # print("2 %d %.2f %d %.2f"%(bw*1000000000, 0.2, bw*4*1000000000, 0.2))
    # ------------------------------------------------------------------------------------
    for loop in range(0, bandLen):
        vKminWidth = bandWidth[loop]*1000000000
        vKmaxRate = 400*bandWidth[loop]/25
        vKminRate = 100*bandWidth[loop]/25
        kmaxStr = kmaxStr + " " + \
            str(int(vKminWidth)) + " " + str(int(vKmaxRate))
        kminStr = kminStr + " " + \
            str(int(vKminWidth)) + " " + str(int(vKminRate))
        pmaxStr = pmaxStr + " " + str(int(vKminWidth)) + " 0.2"
    return kmaxStr, kminStr, pmaxStr


def formatFlowConfig(modeName, jsBandWidth, lossRate):
    global g_curDir
    isErr, topology_path, flow_path, trace_path, trace_output_path, fct_output_path, pfc_output_path, qlen_mon_path = getConfigPath(
        modeName)
    if isErr == False:
        return
    kmaxStr, kminStr, pmaxStr = genBandWidth(modeName, jsBandWidth)
    try:
        with open(g_curDir + "/" + "sim-samp.conf", "r") as file:
            simText = file.read()
            simText = simText.format(topo=topology_path, flow=flow_path, trace=trace_path,
                                     mix=trace_output_path, fct=fct_output_path, pfc=pfc_output_path, qlen=qlen_mon_path, kmax=kmaxStr, kmin=kminStr, pmax=pmaxStr, lrate=lossRate)
            with open(g_curDir + "/" + "sim-formal.conf", "w") as file:
                file.write(simText)
    except FileNotFoundError:
        print("sim-samp.conf文件不存在")
        return
    with open(trace_path, "w") as file:
        file.write("0\n0\n\nFirst line: tracing node #\nNode IDs...\n")


def runSimulation(confPath):
    confPath = "./waf --run \'scratch/third " + confPath + "\'"
    os.system(confPath)
    return


def getFlowList(filePath, colNum):
    out_list = []
    with open(filePath, "r") as file:
        fctText = file.read()
        rowList = fctText.split("\n")
        if len(rowList) <= 0:
            return
        for cellList in rowList:
            cell = cellList.split(" ")
            if len(cell) < 8:
                continue
            out_list.append(int(cell[colNum]))
    return out_list


def getFlowAverage(filePath, colNum):
    add_val = 0
    fctlist = getFlowList(filePath, colNum)
    if len(fctlist) == 0:
        print("Out-fct file has no content ...")
        sys.exit(1)
    for single_val in fctlist:
        add_val += single_val
    return int(add_val/len(fctlist))


def changeNSToMS(nsVal, unit, decimals):
    if unit == "ms":
        nsVal = float(nsVal)/1000000
    elif unit == "us":
        nsVal = float(nsVal)/1000
    elif unit == "s":
        nsVal = float(nsVal)/1000000000
    else:
        nsVal = nsVal
    if decimals == 0:
        return nsVal
    else:
        return round(nsVal, decimals)


def fctSetFlowAndTopo(modeName, nodeCount, jsCompareSet):
    global g_jsRoot
    global g_curDir
    curDir = refixPath(g_curDir,
                       g_jsRoot["flow"][modeName]["conf_path"])
    jsConfName = g_jsRoot["common"]["conf_name"]
    flowPath = refixPath(curDir, jsConfName["flow_file"])
    flowText = str(nodeCount-1) + "\n"
    for loop in range(0, nodeCount-1):
        flowText = flowText + str(loop+2) + " 1 3 100 " + str(
            jsCompareSet["payloadSize"]) + " 2\n"
    with open(flowPath, "w") as file:
        file.write(flowText)
    topoPath = refixPath(curDir, jsConfName["topology_file"])
    topoText = str(nodeCount+1) + " 1 " + str(nodeCount) + "\n0\n"
    for loop in range(0, nodeCount):
        topoText = topoText + "0 " + str(loop+1) + " " + str(
            jsCompareSet["bandWidth"]) + "Gbps " + str(jsCompareSet["linkDelay"]) + "ms 0\n"
    with open(topoPath, "w") as file:
        file.write(topoText)


def parseResultPack(resPack, outPath, unit, decimals):
    global g_isOutExcel
    combineText = ""
    if g_isOutExcel:
        # for excel image
        for cellFlag in resPack.getCellFlagListByIndex(0):
            combineText = combineText + "\t" + str(cellFlag)
        combineText += "\n"
        for cellName in resPack.getCellNameList():
            combineText += cellName
            for cellFlag in resPack.getCellFlagList(cellName):
                _, latency = resPack.getCellData(cellName, cellFlag)
                combineText = combineText + "\t" + \
                    str(changeNSToMS(latency, unit, decimals))
            combineText += "\n"
        with open(outPath, "w") as file:
            file.write(combineText)
    else:
        # for python image
        combineText = "Performance change as the number of QPs/nodes increase\t\tMAX LDR\t\t\n"
        combineText += "Number of QPs on RDMA NIC\tThroughput (Gbps)"
        for cellName in resPack.getCellNameList():
            combineText = combineText + "\t" + cellName
        combineText += "\n"
        bIsFirst = True
        for cellFlag in resPack.getCellFlagListByIndex(0):
            bIsFirst = True
            for cellName in resPack.getCellNameList():
                bandwidth, latency = resPack.getCellData(cellName, cellFlag)
                if bIsFirst == True:
                    combineText += str(cellFlag)
                    combineText = combineText + "\t" + str(bandwidth)
                    bIsFirst = False
                combineText = combineText + "\t" + \
                    str(changeNSToMS(latency, unit, decimals))
            combineText += "\n"
        with open(outPath, "w") as file:
            file.write(combineText)


def parseResultBreakOutPack(resPack, outPath, unit, decimals):
    global g_isOutExcel
    bIsFirst = True
    combineText = ""
    if g_isOutExcel:
        # for excel image
        for cellName in resPack.getCellNameList():
            if not bIsFirst:
                combineText += "\t"
            bIsFirst = False
            combineText += str(cellName)
        combineText += "\n"
        for cellFlag in resPack.getCellFlagListByIndex(0):
            bIsFirst = True
            for cellName in resPack.getCellNameList():
                if not bIsFirst:
                    combineText += "\t"
                bIsFirst = False
                _, value = resPack.getCellData(cellName, cellFlag)
                combineText += str(changeNSToMS(value, unit, decimals))
            combineText += "\n"
        with open(outPath, "w") as file:
            file.write(combineText)
    else:
        # for python image
        return


def calculateBandWidth(resPack, baseName):
    baseBw = {}
    for baseFlag in resPack.getCellFlagList(baseName):
        bandWidth, latency = resPack.getCellData(baseName, baseFlag)
        dataArr = [bandWidth, latency]
        baseBw[baseFlag] = dataArr
    for resName in resPack.getCellNameList():
        if resName == baseName:
            continue
        for resFlag in resPack.getCellFlagList(resName):
            bandWidth, latency = resPack.getCellData(resName, resFlag)
            multi = float(baseBw[resFlag][1])/float(latency)
            latency = float(multi*float(baseBw[resFlag][0]))
            resPack.addCell(resName, resFlag, bandWidth, latency)
    for baseFlag in resPack.getCellFlagList(baseName):
        bandWidth, _ = resPack.getCellData(baseName, baseFlag)
        resPack.addCell(baseName, baseFlag, bandWidth, bandWidth)


def outputResultPackFile(modeName, resPack, fileName):
    global g_jsRoot
    global g_curDir
    parseResultFunc = None
    curDir = refixPath(g_curDir,
                       g_jsRoot["flow"][modeName]["conf_path"])
    outPath = refixPath(curDir, fileName)
    if modeName == "goodput":
        parseResultFunc = parseResultBreakOutPack
    else:
        parseResultFunc = parseResultPack
    parseResultFunc(
        resPack, outPath, g_jsRoot["flow"][modeName]["unit"], g_jsRoot["flow"][modeName]["decimals"])


def flowHandle(modeName):
    global g_jsRoot
    if not g_jsRoot["flow"][modeName]["active"]:
        return
    global g_curDir
    baseName = ""
    resPack = ResPack()
    _, _, _, _, _, flow_output_path, _, _ = getConfigPath(modeName)
    jsStruct = g_jsRoot["flow"][modeName]["struct"]
    structLen = len(jsStruct)
    for loop in range(0, structLen):
        jsCompareSet = g_jsRoot["flow"][modeName]["struct"][loop]["compareSet"]
        compareSetLen = len(jsCompareSet)
        nodeCount = jsStruct[loop]["nodeCount"]
        for loopdup in range(0, compareSetLen):
            if "lossRate" in jsStruct[loop]["compareSet"][loopdup]:
                formatFlowConfig(
                    modeName, jsStruct[loop]["compareSet"][loopdup]["bandWidth"], str(jsStruct[loop]["compareSet"][loopdup]["lossRate"]))
            else:
                formatFlowConfig(
                    modeName, jsStruct[loop]["compareSet"][loopdup]["bandWidth"], "0.0000")
            fctSetFlowAndTopo(modeName, nodeCount,
                              jsStruct[loop]["compareSet"][loopdup])
            runSimulation(refixPath(g_curDir, "sim-formal.conf"))
            if modeName == "fct":
                outVal = getFlowAverage(flow_output_path, 6)
                resPack.addCell(jsStruct[loop]["compareSet"]
                                [loopdup]["descript"], nodeCount, jsStruct[loop]["compareSet"]
                                [loopdup]["bandWidth"], outVal)
            elif modeName == "slowdown":
                avgFctVal = getFlowAverage(flow_output_path, 6)
                avgAlFctVal = getFlowAverage(flow_output_path, 7)
                outVal = float(avgFctVal)/float(avgAlFctVal)
                resPack.addCell(jsStruct[loop]["compareSet"]
                                [loopdup]["descript"], nodeCount, jsStruct[loop]["compareSet"]
                                [loopdup]["bandWidth"], outVal)
            elif modeName == "throughput" or modeName == "goodput":
                #forOutputTestScript(flow_output_path, "/root/code/outfile_"+jsStruct[loop]["compareSet"][loopdup]["descript"] + "_" + str(
                #    jsStruct[loop]["compareSet"][loopdup]["payloadSize"]) + ".txt")
                flagDesc = None
                if "isBase" in jsStruct[loop]["compareSet"][loopdup]:
                    if jsStruct[loop]["compareSet"][loopdup]["isBase"]:
                        baseName = jsStruct[loop]["compareSet"][loopdup]["descript"]
                outVal = getFlowAverage(flow_output_path, 6)
                if modeName == "throughput":
                    flagDesc = jsStruct[loop]["compareSet"][loopdup]["payloadSize"]
                else:
                    flagDesc = jsStruct[loop]["compareSet"][loopdup]["lossRate"]
                resPack.addCell(jsStruct[loop]["compareSet"]
                                [loopdup]["descript"], flagDesc,
                                jsStruct[loop]["compareSet"][loopdup]["bandWidth"], outVal)
            else:
                print("Error modeName ...")
                sys.exit(1)
        if modeName == "throughput" or modeName == "goodput":
            if len(baseName) <= 0:
                print("Never specify throughput base-name ...")
                sys.exit(1)
            calculateBandWidth(resPack, baseName)
            outputResultPackFile(
                modeName, resPack, "out_res_" + str(nodeCount) + ".txt")
    if modeName == "fct" or modeName == "slowdown":
        outputResultPackFile(modeName, resPack, "out_res.txt")


def main():
    global g_curDir
    g_curDir = os.getcwd()
    if not initMainConfig():
        return
    flowHandle("slowdown")
    flowHandle("throughput")
    flowHandle("goodput")
    flowHandle("fct")


if __name__ == "__main__":
    main()
