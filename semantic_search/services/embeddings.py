import os
import logging
import threading
from sentence_transformers import SentenceTransformer

# Model identifier
_MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

# Lock + cached model instance
_lock = threading.Lock()
_model = None

# Reduce verbose HF/transformers logging that produces load reports and warnings
os.environ.setdefault("TRANSFORMERS_NO_ADVISORY_WARNINGS", "1")
for logger_name in ("transformers", "transformers.modeling_utils", "sentence_transformers", "huggingface_hub"):
    logging.getLogger(logger_name).setLevel(logging.ERROR)


def get_model():
    """Lazily load a SentenceTransformer. If an HF token is available via
    environment variables `HF_TOKEN` or `HUGGINGFACE_HUB_TOKEN`, pass it to
    the loader to avoid unauthenticated download warnings and get higher
    rate limits.
    """
    global _model
    if _model is None:
        with _lock:
            if _model is None:
                hf_token = os.getenv("HF_TOKEN") or os.getenv("HUGGINGFACE_HUB_TOKEN")
                if hf_token:
                    _model = SentenceTransformer(_MODEL_NAME, use_auth_token=hf_token)
                else:
                    _model = SentenceTransformer(_MODEL_NAME)
    return _model


def embed_text(text: str) -> list[float]:
    text = (text or "").strip()
    if not text:
        return []
    model = get_model()
    vec = model.encode([text], normalize_embeddings=True)[0]
    return vec.tolist()


def model_name() -> str:
    return _MODEL_NAME