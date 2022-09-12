import sys
import os
import glob
from tqdm import tqdm

poetry = "poetry run python"


def sh(cmd: str):
    print(f">>> {cmd}")
    os.system(cmd)


if __name__ == '__main__':
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    print(f"Converting {input_path} -> {output_path}")

    sh("rm tmp/* -rf")
    in_pic_path = f"tmp/{input_path}"
    os.makedirs(in_pic_path, exist_ok=True)
    out_pic_path = f"tmp/{output_path}"
    os.makedirs(out_pic_path, exist_ok=True)

    command = f"ffmpeg -i {input_path} {in_pic_path}/%04d.png -hide_banner"
    sh(command)

    files = glob.glob(f"{in_pic_path}/*.png")
    for fname in files:
        base = os.path.basename(fname)
        fdir = f"{in_pic_path}/000"
        os.makedirs(fdir, exist_ok=True)
        sh(f"mv {fname} {fdir}/{base}")

    task = "001_VRT_videosr_bi_REDS_6frames"
    command = f"{poetry} main_test_vrt.py --task {task} --folder_lq {in_pic_path} --tile 6 128 128 --tile_overlap 2 20 20"
    sh(command)

    command = f"ffmpeg -framerate 15 -pattern_type glob -i '{out_pic_path}/*.png' -c:v libx264 -pix_fmt yuv420p {output_path}"
    # sh(command)
