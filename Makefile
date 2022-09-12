POETRY = poetry run python

download-all-models:
	$(POETRY) main_download_pretrained_models.py --models "all"  --model_dir "model_zoo"

process-video:
	$(POETRY) video.py input.mp4 output.mp4
