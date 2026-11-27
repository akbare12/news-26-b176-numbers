# main.py — news-image-20261126 entry (b176, numbers).
# Grader is stdlib-only, so this file imports only os/shutil/sys/hashlib.
# It copies the pre-rendered entry.png (built at build time by gen.py)
# into MAKEFUN_OUTPUT_DIR. It never renders, never imports PIL/numpy.
# The copy is verified by SHA-256 so a truncated write cannot pass silently.
import hashlib
import os
import shutil
import sys


def _sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    if not os.path.isfile(src):
        sys.stderr.write("entry.png missing next to main.py\n")
        return 1
    if os.path.getsize(src) > 1024 * 1024:
        sys.stderr.write("entry.png over 1 MiB\n")
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    # Verify the copy byte-for-byte; the grader reads this file, not the repo.
    if _sha256(src) != _sha256(dst):
        sys.stderr.write("sha256 mismatch after copy\n")
        return 1
    sys.stdout.write("copied entry.png (%d bytes) sha256=%s\n"
                     % (os.path.getsize(dst), _sha256(dst)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
