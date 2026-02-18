"""Quick diagnostic for semantic search embeddings and ranking.
Run with: python scripts/debug_semantic_search.py
"""
import os
import math

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django
import sys

# Ensure project root is importable so `config` settings can be found
proj_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, proj_root)

django.setup()

try:
    from semantic_search.services.embeddings import embed_text, model_name
    embed_available = True
except Exception:
    embed_available = False
    embed_text = None
    model_name = lambda: '<embed unavailable>'
 
from events.models import Event
from django.utils import timezone


def main():
    q = 'jo'
    print('Model:', model_name())
    if embed_available:
        q_vec = embed_text(q)
        print('Query vector length:', len(q_vec))
        q_norm = math.sqrt(sum(x*x for x in q_vec)) if q_vec else 0
        print('Query norm:', q_norm)
    else:
        q_vec = None
        print('Embedding functions unavailable in this environment.')

    qs = Event.objects.all()
    future_qs = qs.filter(scheduled_date__gte=timezone.now())
    print('Total events:', qs.count(), 'Future events:', future_qs.count())

    items = []
    for e in qs:
        emb = getattr(e, 'embedding', None)
        if emb and isinstance(emb, list) and len(emb) > 0:
            items.append((e, emb))

    print('Events with embeddings:', len(items))
    if items:
        first_len = len(items[0][1])
        print('Embedding length (sample):', first_len)

    if q_vec is not None:
        # simple pure-Python ranking (avoid numpy dependency here)
        def score_vec(a, b):
            if not a or not b or len(a) != len(b):
                return None
            return sum(x * y for x, y in zip(a, b))

        scored = []
        for ev, emb in items:
            s = score_vec(q_vec, emb)
            if s is not None:
                scored.append((ev, s))

        scored.sort(key=lambda x: x[1], reverse=True)
        print('Ranked results count:', len(scored))
        for i, (ev, score) in enumerate(scored[:10], 1):
            print(f"{i}. {ev.title} — {ev.scheduled_date} — score={score:.4f}")
    else:
        print('Skipping ranking since embed_text is unavailable in this environment.')


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        import traceback
        traceback.print_exc()
        print('Error during diagnostic:', exc)
