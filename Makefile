POETRY = poetry run python

download-all-models:
	$(POETRY) main_download_pretrained_models.py --models "all"  --model_dir "model_zoo"
