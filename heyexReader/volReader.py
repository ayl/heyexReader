#!/usr/bin/env python
#
# Aaron Y. Lee MD MSCI (University of Washington)
#
# Code ported from Markus Mayer's excellent work (https://www5.cs.fau.de/research/software/octseg/)


import struct, array, datetime
import numpy as np
from collections import OrderedDict

class volFile():
    def __init__(self, filename):
        self.__parseVolFile(filename)

    @property
    def oct(self):
        """returns OCT volume as a 3D numpy array.

        Returns:
            3D numpy array with OCT intensities ranging from 0 to 255.

        """
        return self.wholefile["cScan"]

    @property
    def irslo(self):
        return self.wholefile["sloImage"]

    @property
    def fileHeader(self):
        return self.wholefile["header"]

    @property
    def bScanHeader(self, slicei):
        return self.wholefile["slice-headers"][slicei]

    def saveGrid(self, outfn):
        """saves the grid mapping OCT to the IR image.

        Saves the grid coordinates mapping OCT Bscans to the IR SLO image to a text file. The text file
        will be a tab-delimited file with 5 columns: The bscan number, x_0, y_0, x_1, y_1 in pixel space
        scaled to the resolution of the IR SLO image.

        Args:
            wf: whole file object
            outfn (str): location of where to output the file

        Returns:
            None

        """
        grid = self.__getGrid()
        with open(outfn, "w") as fout:
            fout.write("bscan\tx_0\ty_0\tx_1\ty_1\n")
            ri = 0
            for r in grid:
                r = [ri] + r
                fout.write("%s\n" % "\t".join(map(str, r)))
                ri += 1

    def __getGrid(self):
        wf = self.wholefile
        grid = []
        for bi in range(len(wf["slice-headers"])):
            bscanHead = wf["slice-headers"][bi]
            x_0 = int(bscanHead["startX"] / wf["header"]["scaleXSlo"])
            x_1 = int(bscanHead["endX"] / wf["header"]["scaleXSlo"])
            y_0 = int(bscanHead["startY"] / wf["header"]["scaleYSlo"])
            y_1 = int(bscanHead["endY"] / wf["header"]["scaleYSlo"])
            grid.append([x_0, y_0, x_1, y_1])
        return grid

    def renderIRslo(self, filepre = "ir", renderGrid=False):
        from PIL import Image, ImageDraw
        wf = self.wholefile
        a = np.copy(wf["sloImage"])
        if renderGrid:
            a = np.stack((a,)*3, axis=-1)
            a = Image.fromarray(a)
            draw = ImageDraw.Draw(a)
            grid = self.__getGrid(wf)
            for (x_0, y_0, x_1, y_1) in grid:
                draw.line((x_0,y_0, x_1, y_1), fill=(255,0,0), width=3)
            a.save("%s-slo.png" % (filepre))
        else:
            Image.fromarray(a).save("%s-slo.png" % (filepre))

    def renderOCTscans(self, filepre = "oct", renderSeg=False):
        from PIL import Image
        wf = self.wholefile
        for i in range(wf["cScan"].shape[0]):
            a = np.copy(wf["cScan"][i])

            if renderSeg:
                a = np.stack((a,)*3, axis=-1)
                for li in range(wf["segmentations"].shape[0]):
                    for x in range(wf["segmentations"].shape[2]):
                        a[int(wf["segmentations"][li,i,x]),x, li] = 255

            Image.fromarray(a).save("%s-%03d.png" % (filepre, i))

    def __parseVolFile(self, fn):
        wholefile = OrderedDict()
        with open(fn, "rb") as fin:
            header = OrderedDict()
            header["version"] = fin.read(12)
            header["octSizeX"] = struct.unpack("I", fin.read(4))[0] # lateral resolution
            header["numBscan"] = struct.unpack("I", fin.read(4))[0]
            header["octSizeZ"] = struct.unpack("I", fin.read(4))[0] # OCT depth
            header["scaleX"] = struct.unpack("d", fin.read(8))[0]
            header["distance"] = struct.unpack("d", fin.read(8))[0]
            header["scaleZ"] = struct.unpack("d", fin.read(8))[0]
            header["sizeXSlo"] = struct.unpack("I", fin.read(4))[0]
            header["sizeYSlo"] = struct.unpack("I", fin.read(4))[0]
            header["scaleXSlo"] = struct.unpack("d", fin.read(8))[0]
            header["scaleYSlo"] = struct.unpack("d", fin.read(8))[0]
            header["fieldSizeSlo"] = struct.unpack("I", fin.read(4))[0] # FOV in degrees
            header["scanFocus"] = struct.unpack("d", fin.read(8))[0]
            header["scanPos"] = fin.read(4)
            header["examTime"] = struct.unpack("l", fin.read(8))[0] / 1e7
            header["examTime"] = datetime.datetime.utcfromtimestamp(header["examTime"] - (369*365.25+4) * 24*60*60) # needs to be checked
            header["scanPattern"] = struct.unpack("I", fin.read(4))[0]
            header["BscanHdrSize"] = struct.unpack("I", fin.read(4))[0]
            header["ID"] = fin.read(16)
            header["ReferenceID"] = fin.read(16)
            header["PID"] = struct.unpack("I", fin.read(4))[0] 
            header["PatientID"] = fin.read(21)
            header["unknown2"] = fin.read(3)
            header["DOB"] = struct.unpack("d", fin.read(8))[0] - 25569
            header["DOB"] = datetime.datetime.utcfromtimestamp(header["DOB"] * 24 * 60 * 60 ) # needs to be checked
            header["VID"] = struct.unpack("I", fin.read(4))[0]
            header["VisitID"] = fin.read(24)
            header["VisitDate"] = struct.unpack("d", fin.read(8))[0] - 25569
            header["VisitDate"] = datetime.datetime.utcfromtimestamp(header["VisitDate"] * 24 * 60 * 60 ) # needs to be checked
            header["GridType"] = struct.unpack("I", fin.read(4))[0]
            header["GridOffset"] = struct.unpack("I", fin.read(4))[0]

            wholefile["header"] = header
            fin.seek(2048)
            U = array.array("B")
            U.fromstring(fin.read(header["sizeXSlo"] * header["sizeYSlo"]))
            U = np.array(U).astype("uint8").reshape((header["sizeXSlo"],header["sizeYSlo"]))
            wholefile["sloImage"] = U

            sloOffset = 2048 + header["sizeXSlo"] * header["sizeYSlo"]
            octOffset = header["BscanHdrSize"] + header["octSizeX"] * header["octSizeZ"] * 4 
            bscans = []
            bscanheaders = []
            segmentations = None
            for i in range(header["numBscan"]):
                fin.seek(16 + sloOffset + i * octOffset)
                bscanHead = OrderedDict()
                bscanHead["startX"] = struct.unpack("d", fin.read(8))[0]
                bscanHead["startY"] = struct.unpack("d", fin.read(8))[0]
                bscanHead["endX"] = struct.unpack("d", fin.read(8))[0]
                bscanHead["endY"] = struct.unpack("d", fin.read(8))[0]
                bscanHead["numSeg"] = struct.unpack("I", fin.read(4))[0]
                bscanHead["offSeg"] = struct.unpack("I", fin.read(4))[0]
                bscanHead["quality"] = struct.unpack("f", fin.read(4))[0]
                bscanHead["shift"] = struct.unpack("I", fin.read(4))[0]
                bscanheaders.append(bscanHead)

                # extract OCT B scan data
                fin.seek(header["BscanHdrSize"] + sloOffset + i * octOffset)
                U = array.array("f")
                U.fromstring(fin.read(4 * header["octSizeX"] * header["octSizeZ"]))
                U = np.array(U).reshape((header["octSizeZ"],header["octSizeX"]))
                # remove out of boundary 
                v = struct.unpack("f", 'FFFF7F7F'.decode("hex"))
                U[U == v] = 0
                # log normalize
                U = np.log(10000 * U + 1)
                U = (255. * (np.clip(U, 0, np.max(U)) / np.max(U))).astype("uint8")
                bscans.append(U)

                # extract OCT segmentations data
                fin.seek(256 + sloOffset + i * octOffset)
                U = array.array("f")
                U.fromstring(fin.read(4 * header["octSizeX"] * bscanHead["numSeg"]))
                U = np.array(U)
                U[U == v] = 0.

                if segmentations == None:
                    segmentations = []
                    for j in range(bscanHead["numSeg"]):
                        segmentations.append([])

                for j in range(bscanHead["numSeg"]):
                    segmentations[j].append(U[j*header["octSizeX"]:(j+1) * header["octSizeX"]].tolist())


            wholefile["cScan"] = np.array(bscans)
            wholefile["segmentations"] = np.array(segmentations)
            wholefile["slice-headers"] = bscanheaders
            self.wholefile = wholefile
