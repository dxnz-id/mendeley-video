#!/usr/bin/env python3
import argparse
import json
import math
import re
import subprocess
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
AUDIO = ROOT / "assets" / "audio"
MEDIA = ROOT / "media"
FINAL = ROOT / "mendeley-tutorial.mp4"
SRT = ROOT / "mendeley-tutorial.srt"
TIMING = ROOT / "timing.json"
SCRIPT = ROOT / "script.json"
TTS_BIN = ROOT / "node_modules" / "node-edge-tts" / "bin.js"
RESOLUTION = "1920,1080"
FPS = 30


def run(cmd, **kwargs):
    return subprocess.run(cmd, check=True, **kwargs)


def probe_duration(path):
    out = subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nw=1:nk=1", str(path)],
        text=True,
    ).strip()
    return float(out)


def norm(text):
    return re.sub(r"[^a-z0-9]+", "", text.lower())


def find_cue(words, cue):
    target = norm(cue["match"])
    hits = [w for w in words if norm(w["part"]) == target]
    occurrence = int(cue.get("occurrence", 1))
    if len(hits) >= occurrence:
        return hits[occurrence - 1]["start"] / 1000.0
    fallback = cue.get("fallback")
    if fallback:
        fallback_target = norm(fallback)
        hits = [w for w in words if norm(w["part"]) == fallback_target]
        if hits:
            return hits[0]["start"] / 1000.0
    spoken = " ".join(w["part"].strip() for w in words)
    raise ValueError(
        f"Cue '{cue['key']}' ({cue['match']}) not found in: {spoken}"
    )


def make_tts(scene, cfg):
    out = AUDIO / f"{scene['id']}.mp3"
    cmd = [
        "node", str(TTS_BIN),
        "-t", scene["narration"],
        "-f", str(out),
        "-v", cfg["voice"],
        "-l", cfg["locale"],
        "-r", cfg["rate"],
        "-s",
        "--timeout", "60000",
    ]
    for attempt in range(3):
        try:
            run(cmd, stdout=subprocess.DEVNULL)
            if not out.exists() or out.stat().st_size == 0:
                raise RuntimeError("empty TTS output")
            words = json.loads(Path(str(out) + ".json").read_text())
            return out, words
        except (subprocess.CalledProcessError, RuntimeError, json.JSONDecodeError):
            if attempt == 2:
                raise
            out.unlink(missing_ok=True)
            Path(str(out) + ".json").unlink(missing_ok=True)
            time.sleep(1)
    raise RuntimeError("unreachable")


def srt_time(seconds):
    ms = int(round(seconds * 1000))
    hours, ms = divmod(ms, 3_600_000)
    minutes, ms = divmod(ms, 60_000)
    secs, ms = divmod(ms, 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{ms:03d}"


def subtitle_cues(words, scene_offset, lead_in):
    groups, current = [], []
    for word in words:
        if current:
            gap = word["start"] / 1000.0 - current[-1]["end"] / 1000.0
            text_len = len(" ".join(w["part"].strip() for w in current))
            if gap > 0.6 or len(current) >= 9 or text_len >= 42:
                groups.append(current)
                current = []
        current.append(word)
        if re.search(r"[.!?]$", word["part"].strip()) and len(current) >= 2:
            groups.append(current)
            current = []
    if current:
        groups.append(current)

    cues = []
    for group in groups:
        start = scene_offset + lead_in + group[0]["start"] / 1000.0
        end = scene_offset + lead_in + group[-1]["end"] / 1000.0
        text = " ".join(w["part"].strip() for w in group)
        text = re.sub(r"\s+([,.!?;:])", r"\1", text).strip()
        cues.append((start, end, text))
    return cues


def build_timing():
    cfg = json.loads(SCRIPT.read_text())
    AUDIO.mkdir(parents=True, exist_ok=True)
    timeline = {}
    srt_lines = []
    offset = 0.0
    srt_index = 1

    print(f"{'Scene':8} {'narration':>10} {'scene':>8}  cues")
    for scene in cfg["scenes"]:
        audio, words = make_tts(scene, cfg)
        narration = probe_duration(audio)
        lead_in = float(cfg["lead_in"])
        tail = float(cfg["tail"])
        duration = max(float(scene["min_duration"]), narration + lead_in + tail)
        duration = math.ceil(duration * 10) / 10.0

        cues = {}
        for cue in scene.get("cues", []):
            cues[cue["key"]] = round(find_cue(words, cue), 3)

        timeline[scene["id"]] = {
            "duration": duration,
            "narration_duration": round(narration, 3),
            "audio": str(audio.relative_to(ROOT)),
            "cues": cues,
        }
        cue_text = " ".join(f"{k}={v:.2f}" for k, v in cues.items())
        print(f"{scene['id']:8} {narration:10.2f} {duration:8.1f}  {cue_text}")

        for start, end, text in subtitle_cues(words, offset, lead_in):
            srt_lines.append(f"{srt_index}\n{srt_time(start)} --> {srt_time(end)}\n{text}\n")
            srt_index += 1
        offset += duration

    TIMING.write_text(json.dumps(timeline, indent=2, ensure_ascii=False) + "\n")
    SRT.write_text("\n".join(srt_lines), encoding="utf-8")
    print(f"\nTotal video: {offset:.1f}s ({offset/60:.2f} min)")
    print(f"Wrote {TIMING.name}, {SRT.name}, and {len(timeline)} audio files.")


def render_scenes(only=None):
    timing = json.loads(TIMING.read_text())
    ids = [s["id"] for s in json.loads(SCRIPT.read_text())["scenes"]]
    if only:
        wanted = {x.strip() for x in only.split(",")}
        ids = [x for x in ids if x in wanted]
    cmd = [
        "manim", "-r", RESOLUTION, "--fps", str(FPS),
        "--disable_caching", "--media_dir", str(MEDIA),
        str(ROOT / "scenes" / "video.py"), *ids,
    ]
    print("Rendering:", " ".join(ids))
    run(cmd)
    for scene_id in ids:
        path = MEDIA / "videos" / "video" / "1080p30" / f"{scene_id}.mp4"
        if not path.exists():
            raise FileNotFoundError(path)
        actual = probe_duration(path)
        expected = timing[scene_id]["duration"]
        print(f"{scene_id}: {actual:.2f}s (target {expected:.2f}s)")
        if abs(actual - expected) > 0.12:
            raise ValueError(f"{scene_id} duration mismatch: {actual:.2f} vs {expected:.2f}")


def assemble():
    timing = json.loads(TIMING.read_text())
    scenes = json.loads(SCRIPT.read_text())["scenes"]
    ids = [s["id"] for s in scenes]
    video_paths = [MEDIA / "videos" / "video" / "1080p30" / f"{i}.mp4" for i in ids]
    for path in video_paths:
        if not path.exists():
            raise FileNotFoundError(path)

    video_list = ROOT / "video_concat.txt"
    video_list.write_text("".join(f"file '{p}'\n" for p in video_paths))
    silent = ROOT / "video_silent.mp4"
    run([
        "ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0",
        "-i", str(video_list), "-c", "copy", str(silent),
    ])

    lead_in = 0.4
    audio_paths = []
    for scene in scenes:
        scene_id = scene["id"]
        duration = timing[scene_id]["duration"]
        src = ROOT / timing[scene_id]["audio"]
        out = AUDIO / f"{scene_id}.wav"
        run([
            "ffmpeg", "-y", "-v", "error", "-i", str(src),
            "-af", f"adelay={int(lead_in*1000)}:all=1,apad=whole_dur={duration}",
            "-t", f"{duration:.3f}", "-ar", "48000", "-ac", "1", str(out),
        ])
        audio_paths.append(out)

    audio_list = ROOT / "audio_concat.txt"
    audio_list.write_text("".join(f"file '{p}'\n" for p in audio_paths))
    full_audio = ROOT / "narration.wav"
    run([
        "ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0",
        "-i", str(audio_list), "-c:a", "pcm_s16le", str(full_audio),
    ])

    run([
        "ffmpeg", "-y", "-v", "error", "-i", str(silent), "-i", str(full_audio),
        "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", str(FINAL),
    ])
    print(f"Wrote {FINAL.name}: {probe_duration(FINAL):.2f}s")
    print(f"Wrote {SRT.name}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--render", action="store_true", help="render all scenes and assemble")
    parser.add_argument("--only", help="render only these scene ids, comma separated")
    parser.add_argument("--assemble", action="store_true", help="assemble existing scene renders")
    args = parser.parse_args()

    if not TIMING.exists() or not args.assemble:
        build_timing()
    if args.render or args.only:
        render_scenes(args.only)
    if args.render or args.assemble:
        if not args.only:
            assemble()


if __name__ == "__main__":
    main()
