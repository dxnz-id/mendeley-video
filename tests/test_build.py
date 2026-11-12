import math
import subprocess
import tempfile
import unittest
import wave
from pathlib import Path

import build


class TimingTests(unittest.TestCase):
    def test_split_subtitle_preserves_words(self):
        text = "Menulis sitasi secara manual berarti mengetik sumber yang sama dua kali."
        chunks = build.split_subtitle(text)
        self.assertEqual(" ".join(chunks), text)
        for chunk in chunks:
            self.assertLessEqual(len(chunk), 42)
            self.assertLessEqual(len(chunk.split()), 9)

    def test_align_lines_uses_pauses(self):
        lines = [{"text": "satu dua tiga empat"} for _ in range(3)]
        starts, ends = build.align_lines(
            lines, 10.0, [(2.8, 3.2), (6.0, 6.4)]
        )
        self.assertAlmostEqual(starts[0], 0.0)
        self.assertAlmostEqual(ends[0], 2.8)
        self.assertAlmostEqual(starts[1], 3.2)
        self.assertAlmostEqual(ends[1], 6.0)
        self.assertAlmostEqual(starts[2], 6.4)
        self.assertAlmostEqual(ends[2], 10.0)

    def test_detect_silences(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "tone.wav"
            rate = 24000
            with wave.open(str(path), "wb") as wav:
                wav.setnchannels(1)
                wav.setsampwidth(2)
                wav.setframerate(rate)
                frames = bytearray()
                for i in range(int(rate * 1.8)):
                    t = i / rate
                    if 0.5 <= t < 1.3:
                        value = int(0.3 * 32767 * math.sin(2 * math.pi * 440 * t))
                    else:
                        value = 0
                    frames.extend(int(value).to_bytes(2, "little", signed=True))
                wav.writeframes(bytes(frames))
            silences = build.detect_silences(path)
            self.assertTrue(any(abs(end - 0.5) < 0.1 for _, end in silences))
            self.assertTrue(any(abs(start - 1.3) < 0.1 for start, _ in silences))


if __name__ == "__main__":
    unittest.main()
