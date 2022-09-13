import sys
import os
import glob
from tqdm import tqdm
from logging import info
import coloredlogs

coloredlogs.install(level='INFO')

poetry = "poetry run python"


def sh(cmd: str):
    info(f">>> {cmd}")
    os.system(cmd)


if __name__ == '__main__':
    n = "000"
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    info(f"Converting {input_path} -> {output_path}")

    sh("rm tmp/* -rf")
    in_pic_path = f"tmp/{input_path}"
    os.makedirs(in_pic_path, exist_ok=True)
    out_pic_path = f"tmp/{output_path}"
    os.makedirs(out_pic_path, exist_ok=True)

    command = f"ffmpeg -i {input_path} -qscale:v 1 -qmin 1 -qmax 1 -vsync 0 {in_pic_path}/%04d.png -hide_banner"
    sh(command)

    files = glob.glob(f"{in_pic_path}/*.png")
    for fname in files:
        base = os.path.basename(fname)
        fdir = f"{in_pic_path}/{n}"
        os.makedirs(fdir, exist_ok=True)
        sh(f"mv {fname} {fdir}/{base}")

    # task = "001_VRT_videosr_bi_REDS_6frames" # done
    task = "002_VRT_videosr_bi_REDS_16frames"  # done
    # task = "003_VRT_videosr_bi_Vimeo_7frames"  # done
    # task = "004_VRT_videosr_bd_Vimeo_7frames"
    # task = "005_VRT_videodeblurring_DVD"
    # task = "006_VRT_videodeblurring_GoPro"
    # task = "007_VRT_videodeblurring_REDS"
    # task = "008_VRT_videodenoising_DAVIS"

    command = f"{poetry} main_test_vrt.py --task {task} --folder_lq {in_pic_path} --tile 6 128 128 --tile_overlap 2 20 20"
    sh(command)

    command = f"ffmpeg -y -framerate 30 -pattern_type glob -i 'results/{task}/{n}/*.png' -c:v libx264 -pix_fmt yuv420p {output_path}"
    sh(command)
    sh(f"cp -f output.mp4 outputs/{task}.mp4")
