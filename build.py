#!/usr/bin/env python3
import argparse
import base64
import hashlib
import json
import math
import re
import subprocess
import time
import urllib.error
import urllib.request
import wave
from pathlib import Path

ROOT = Path(__file__).resolve().parent
AUDIO = ROOT / "assets" / "audio"
MEDIA = ROOT / "media"
FINAL = ROOT / "mendeley-tutorial.mp4"
SRT = ROOT / "mendeley-tutorial.srt"
TIMING = ROOT / "timing.json"
SCRIPT = ROOT / "script.json"
POCKET_BIN = ROOT / "tools" / "go-pocket-tts" / "pockettts"
POCKET_DIR = ROOT / "tools" / "pockettts" / "indonesian"
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


def text_hash(text):
    return hashlib.sha1(text.encode("utf-8")).hexdigest()


def cache_meta_path(audio_path):
    return Path(str(audio_path) + ".json")


def cached_audio(scene, text, engine, cfg, force=False):
    audio_path = AUDIO / f"{scene['id']}.wav"
    meta_path = cache_meta_path(audio_path)
    if force or not audio_path.exists() or not meta_path.exists():
        return None
    try:
        meta = json.loads(meta_path.read_text())
    except json.JSONDecodeError:
        return None
    if meta.get("text_hash") != text_hash(text):
        return None
    if meta.get("engine") != engine:
        return None
    if engine == "mengetik" and meta.get("voice") != cfg["voice"]:
        return None
    if engine == "pockettts" and meta.get("voice") != cfg["pocket_voice"]:
        return None
    return audio_path


def write_audio_meta(audio_path, scene, text, engine, cfg):
    meta = {
        "scene": scene["id"],
        "engine": engine,
        "voice": cfg["voice"] if engine == "mengetik" else cfg["pocket_voice"],
        "text_hash": text_hash(text),
        "text": text,
    }
    cache_meta_path(audio_path).write_text(
        json.dumps(meta, indent=2, ensure_ascii=False) + "\n"
    )


def tts_mengetik(text, out_path, cfg):
    payload = {
        "action": "tts",
        "text": text,
        "voice": cfg["voice"],
        "gender": cfg["gender"],
        "style": cfg["style"],
        "styleText": cfg["style_text"],
        "token": cfg["mengetik_token"],
        "client": cfg["mengetik_client"],
    }
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    last_error = None
    for attempt in range(3):
        req = urllib.request.Request(
            cfg["mengetik_url"],
            data=body,
            headers={"Content-Type": "application/json"},
        )
        try:
            raw = urllib.request.urlopen(req, timeout=300).read()
            data = json.loads(raw)
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
            last_error = exc
            if attempt < 2:
                time.sleep(3 * (attempt + 1))
                continue
            raise RuntimeError(f"Mengetik TTS gagal: {exc}") from exc

        if not data.get("ok"):
            code = str(data.get("error", "unknown"))
            if code in {"daily", "quota"}:
                raise RuntimeError(
                    f"Kuota Mengetik habis ({code}). Coba lagi setelah 15.00 WIB, "
                    "atau jalankan dengan --engine pockettts."
                )
            last_error = RuntimeError(f"{code}: {data.get('detail', '')}")
            if attempt < 2:
                time.sleep(3 * (attempt + 1))
                continue
            raise last_error

        audio = base64.b64decode(data["audio"])
        if data.get("format") == "wav" or audio[:4] == b"RIFF":
            out_path.write_bytes(audio)
        else:
            rate = int(data.get("rate", 24000))
            with wave.open(str(out_path), "wb") as wav:
                wav.setnchannels(1)
                wav.setsampwidth(2)
                wav.setframerate(rate)
                wav.writeframes(audio)

        if not out_path.exists() or out_path.stat().st_size == 0:
            raise RuntimeError("Mengetik TTS menghasilkan file kosong")
        return out_path

    raise RuntimeError(f"Mengetik TTS gagal: {last_error}")


def tts_pockettts(text, out_path, cfg):
    if not POCKET_BIN.exists():
        raise FileNotFoundError(f"Binary Pocket TTS tidak ada: {POCKET_BIN}")
    voice = ROOT / cfg["pocket_voice"]
    if not voice.exists():
        raise FileNotFoundError(f"Voice Pocket TTS tidak ada: {voice}")
    run([
        str(POCKET_BIN), "synth",
        "--model-config", str(POCKET_DIR / "config.yaml"),
        "--paths-model-path", str(POCKET_DIR / "model.safetensors"),
        "--paths-tokenizer-model", str(POCKET_DIR / "tokenizer.model"),
        "--voice", str(voice),
        "--text", text,
        "--out", str(out_path),
        "--normalize",
    ], stdout=subprocess.DEVNULL, timeout=1800)
    if not out_path.exists() or out_path.stat().st_size == 0:
        raise RuntimeError("Pocket TTS menghasilkan file kosong")
    return out_path


def make_tts(scene, cfg, engine, force=False):
    text = " ".join(line["text"] for line in scene["lines"])
    cached = cached_audio(scene, text, engine, cfg, force=force)
    if cached is not None:
        print(f"{scene['id']}: audio cache")
        return cached

    out = AUDIO / f"{scene['id']}.wav"
    out.unlink(missing_ok=True)
    if engine == "mengetik":
        tts_mengetik(text, out, cfg)
    elif engine == "pockettts":
        tts_pockettts(text, out, cfg)
    else:
        raise ValueError(f"Engine TTS tidak dikenal: {engine}")
    write_audio_meta(out, scene, text, engine, cfg)
    return out


def detect_silences(path, noise_db=-35, min_duration=0.22):
    cmd = [
        "ffmpeg", "-hide_banner", "-nostats", "-i", str(path),
        "-af", f"silencedetect=noise={noise_db}dB:d={min_duration}",
        "-f", "null", "-",
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    events = re.findall(r"silence_(start|end):\s*([\d.]+)", proc.stderr)
    result = []
    open_start = None
    for kind, value in events:
        if kind == "start":
            open_start = float(value)
        elif open_start is not None:
            result.append((open_start, float(value)))
            open_start = None
    if open_start is not None:
        result.append((open_start, probe_duration(path)))
    return result


def line_weights(lines):
    weights = []
    for line in lines:
        letters = re.sub(r"[^0-9A-Za-zÀ-ÿ]+", "", line["text"])
        weights.append(max(1, len(letters)) + 4)
    return weights


def align_lines(lines, duration, silences, min_pause=0.18):
    """Return speech start/end per line using the pauses nearest each expected boundary."""
    n = len(lines)
    if n == 1:
        return [0.0], [duration]

    weights = line_weights(lines)
    total = sum(weights)
    pauses = [
        (start, end)
        for start, end in silences
        if start > 0.25 and end < duration - 0.25 and end - start >= min_pause
    ]

    starts = [0.0]
    ends = []
    prev_speech_start = 0.0
    for i in range(n - 1):
        expected = duration * sum(weights[: i + 1]) / total
        candidates = [p for p in pauses if p[0] > prev_speech_start + 0.35]
        if candidates:
            prev_end, next_start = min(
                candidates,
                key=lambda pair: abs(pair[0] - expected),
            )
            if abs(prev_end - expected) > 2.0:
                prev_end = next_start = expected
        else:
            prev_end = next_start = expected

        prev_end = max(prev_end, prev_speech_start + 0.15)
        next_start = max(next_start, prev_end + 0.05)
        ends.append(prev_end)
        starts.append(next_start)
        prev_speech_start = next_start

    last_end = duration
    for start, end in reversed(silences):
        if end >= duration - 0.05 and start > duration - 1.0:
            last_end = start
            break
    last_end = max(last_end, prev_speech_start + 0.15)
    ends.append(last_end)
    return starts, ends


def split_subtitle(text, max_chars=42, max_words=9):
    words = text.split()
    chunks, current = [], []
    for word in words:
        candidate = " ".join(current + [word])
        if current and (len(candidate) > max_chars or len(current) >= max_words):
            chunks.append(" ".join(current))
            current = [word]
        else:
            current.append(word)
    if current:
        chunks.append(" ".join(current))
    return chunks


def subtitle_times(text, start, end):
    chunks = split_subtitle(text)
    if not chunks:
        return []
    total = sum(max(1, len(chunk)) for chunk in chunks)
    cursor = start
    cues = []
    for i, chunk in enumerate(chunks):
        if i == len(chunks) - 1:
            cue_end = end
        else:
            cue_end = cursor + (end - start) * max(1, len(chunk)) / total
        cues.append((cursor, cue_end, chunk))
        cursor = cue_end
    return cues


def srt_time(seconds):
    ms = int(round(seconds * 1000))
    hours, ms = divmod(ms, 3_600_000)
    minutes, ms = divmod(ms, 60_000)
    secs, ms = divmod(ms, 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{ms:03d}"


def draft_timing():
    cfg = json.loads(SCRIPT.read_text())
    AUDIO.mkdir(parents=True, exist_ok=True)
    timeline = {}
    for scene in cfg["scenes"]:
        duration = float(scene["min_duration"])
        weights = line_weights(scene["lines"])
        total = sum(weights)
        cursor = 0.0
        cues = {}
        for line, weight in zip(scene["lines"], weights):
            if line.get("cue"):
                cues[line["cue"]] = round(cursor, 3)
            cursor += duration * weight / total
        timeline[scene["id"]] = {
            "duration": duration,
            "narration_duration": round(duration - cfg["lead_in"] - cfg["tail"], 3),
            "audio": str((AUDIO / f"{scene['id']}.wav").relative_to(ROOT)),
            "cues": cues,
            "draft": True,
        }
    TIMING.write_text(json.dumps(timeline, indent=2, ensure_ascii=False) + "\n")
    print(f"Wrote draft {TIMING.name}; belum ada audio.")


def build_timing(engine, force_tts=False):
    cfg = json.loads(SCRIPT.read_text())
    AUDIO.mkdir(parents=True, exist_ok=True)
    timeline = {}
    srt_lines = []
    offset = 0.0
    srt_index = 1
    lead_in = float(cfg["lead_in"])
    tail = float(cfg["tail"])

    print(f"TTS engine: {engine}; voice: {cfg['voice'] if engine == 'mengetik' else cfg['pocket_voice']}")
    print(f"{'Scene':8} {'narration':>10} {'scene':>8}  cues")
    for scene in cfg["scenes"]:
        audio = make_tts(scene, cfg, engine, force=force_tts)
        narration = probe_duration(audio)
        pocket = engine == "pockettts"
        silences = detect_silences(
            audio,
            noise_db=-30 if pocket else -35,
            min_duration=0.12 if pocket else 0.22,
        )
        starts, ends = align_lines(
            scene["lines"], narration, silences,
            min_pause=0.12 if pocket else 0.18,
        )
        duration = max(float(scene["min_duration"]), narration + lead_in + tail)
        duration = math.ceil(duration * 10) / 10.0

        cues = {}
        for i, line in enumerate(scene["lines"]):
            if line.get("cue"):
                # Sedikit antisipasi agar animasi mulai sebelum suku kata pertama.
                cues[line["cue"]] = round(max(0.0, starts[i] - 0.15), 3)

        timeline[scene["id"]] = {
            "duration": duration,
            "narration_duration": round(narration, 3),
            "audio": str(audio.relative_to(ROOT)),
            "cues": cues,
        }
        cue_text = " ".join(f"{k}={v:.2f}" for k, v in cues.items())
        print(f"{scene['id']:8} {narration:10.2f} {duration:8.1f}  {cue_text}")

        for i, line in enumerate(scene["lines"]):
            for start, end, text in subtitle_times(
                line["text"], starts[i], ends[i]
            ):
            # Hindari subtitle yang mulai sebelum audio scene.
                start = max(0.0, start)
                end = max(start + 0.15, end)
                srt_lines.append(
                    f"{srt_index}\n{srt_time(offset + lead_in + start)} --> "
                    f"{srt_time(offset + lead_in + end)}\n{text}\n"
                )
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
    cfg = json.loads(SCRIPT.read_text())
    timing = json.loads(TIMING.read_text())
    scenes = cfg["scenes"]
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

    lead_in = float(cfg["lead_in"])
    audio_paths = []
    for scene in scenes:
        scene_id = scene["id"]
        duration = timing[scene_id]["duration"]
        src = ROOT / timing[scene_id]["audio"]
        out = AUDIO / f"{scene_id}_pad.wav"
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
    cfg = json.loads(SCRIPT.read_text())
    parser = argparse.ArgumentParser()
    parser.add_argument("--render", action="store_true", help="render all scenes and assemble")
    parser.add_argument("--only", help="render only these scene ids, comma separated")
    parser.add_argument("--assemble", action="store_true", help="assemble existing scene renders")
    parser.add_argument("--audio", action="store_true", help="make TTS audio, timing, and SRT only")
    parser.add_argument("--draft", action="store_true", help="write draft timing without TTS")
    parser.add_argument("--engine", choices=["mengetik", "pockettts"],
                        default=cfg["tts_engine"], help="TTS engine override")
    parser.add_argument("--force-tts", action="store_true", help="ignore TTS cache")
    args = parser.parse_args()

    if args.draft:
        draft_timing()
        return
    if args.only:
        render_scenes(args.only)
        return
    if args.audio or args.render or not TIMING.exists():
        build_timing(args.engine, force_tts=args.force_tts)
    if args.render:
        render_scenes()
    if args.render or args.assemble:
        assemble()


if __name__ == "__main__":
    main()
