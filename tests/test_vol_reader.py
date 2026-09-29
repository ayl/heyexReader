"""Read a synthetic VOL file without relying on patient data or GUI access."""

import struct
import tempfile
import unittest
from pathlib import Path

import numpy as np
from PIL import Image

import heyexReader


def write_test_volume(path):
    """Write one 4x4 scan with three segmentation lines and a 4x4 SLO."""
    header = bytearray(b"HSF-OCT-103\x00")

    def append(fmt, *values):
        header.extend(struct.pack("<" + fmt, *values))

    append("III", 4, 1, 4)  # OCT width, scan count, depth
    append("ddd", 0.01, 0.1, 0.0039)  # scaleX, distance, scaleZ
    append("II", 4, 4)  # SLO width and height
    append("dd", 0.01, 0.01)  # SLO scale
    append("I", 30)  # field size
    append("d", 0.0)  # scan focus
    append("4s", b"OS\x00\x00")
    append("q", 116444736000000000)  # 1970-01-01 in Windows FILETIME units
    append("II", 1, 304)  # scan pattern, B-scan header including segmentations
    append("16s16sI21s3s", b"synthetic", b"", 0, b"synthetic", b"")
    append("d", 25569.0)  # birth date: 1970-01-01
    append("I24sdII", 0, b"synthetic", 25569.0, 0, 0)
    header.extend(bytes(2048 - len(header)))

    slo = bytes(range(16))
    scan_header = bytearray(304)
    struct.pack_into("<ddddIIfI", scan_header, 16,
                     0.0, 0.0, 0.03, 0.03, 3, 256, 1.0, 0)
    struct.pack_into("<12f", scan_header, 256,
                     *([0.0] * 4 + [1.0] * 4 + [2.0] * 4))
    pixels = struct.pack("<16f", *([0.0, 1.0, 0.0, 1.0] * 4))
    path.write_bytes(header + slo + scan_header + pixels)


class VolReaderCompatibilityTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.directory = Path(self.temp.name)
        self.path = self.directory / "synthetic.vol"
        write_test_volume(self.path)

    def test_reads_slo_oct_and_segmentation_buffers(self):
        # Importing alone misses the array.fromstring failure on Python >=3.9.
        volume = heyexReader.volFile(str(self.path))
        np.testing.assert_array_equal(
            volume.irslo, np.arange(16, dtype=np.uint8).reshape(4, 4))
        expected_oct = np.tile([0, 255, 0, 255], (1, 4, 1)).astype(np.uint8)
        np.testing.assert_array_equal(volume.oct, expected_oct)
        self.assertEqual(volume.oct.dtype, np.dtype("uint8"))
        np.testing.assert_array_equal(
            volume.wholefile["segmentations"],
            np.array([[[0] * 4], [[1] * 4], [[2] * 4]]))
        self.assertEqual(volume.fileHeader["scaleX"], 0.01)
        self.assertEqual(volume.fileHeader["scaleZ"], 0.0039)
        self.assertEqual(volume.grid, [[0, 0, 3, 3]])

    def test_renders_pngs_with_segmentation(self):
        volume = heyexReader.volFile(str(self.path))
        volume.renderIRslo(str(self.directory / "slo.png"), renderGrid=True)
        volume.renderOCTscans(str(self.directory / "oct"), renderSeg=True)
        with Image.open(self.directory / "slo.png") as image:
            self.assertEqual(image.format, "PNG")
            self.assertEqual(image.size, (4, 4))
        with Image.open(self.directory / "oct-000.png") as image:
            expected = np.repeat(volume.oct[0, :, :, None], 3, axis=2)
            for row, channel in enumerate(range(3)):
                expected[row, :, channel] = 255
            np.testing.assert_array_equal(np.asarray(image), expected)


if __name__ == "__main__":
    unittest.main()
