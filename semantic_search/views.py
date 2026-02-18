from django.shortcuts import render
from django.utils import timezone

from events.models import Event
from .services.embeddings import embed_text, model_name
from .services.ranker import cosine_top_k

def _event_text(e: Event) -> str:
    parts = [
        e.title or "",
        e.description or "",
        e.category or "",
        e.tags or "",
    ]
    return " | ".join([p.strip() for p in parts if p and p.strip()])

def semantic_search(request):
    q = (request.GET.get("q") or "").strip()
    # If this is the initial blank GET (no params), default to showing only future events.
    # But when the user submits the form (request.GET non-empty), respect the checkbox value.
    if request.GET:
        only_future = request.GET.get("future") == "1"
    else:
        only_future = True

    results = []
    if q:
        q_vec = embed_text(q)

        qs = Event.objects.all()
        if only_future:
            qs = qs.filter(scheduled_date__gte=timezone.now())

        items = []
        missing = []
        for e in qs:
            emb = getattr(e, "embedding", None)
            if emb:
                items.append((e, emb))
            else:
                missing.append(e)

        # If no events have stored embeddings, compute embeddings on-the-fly
        # for the missing events (do not persist). This allows search to work
        # immediately even without a full backfill.
        if not items and missing:
            for e in missing:
                text = _event_text(e)
                if not text:
                    continue
                try:
                    vec = embed_text(text)
                except Exception:
                    vec = None
                if vec:
                    items.append((e, vec))

        ranked = cosine_top_k(q_vec, items, k=20)
        results = ranked

    context = {
        "query": q,
        "results": results,
        "only_future": only_future,
        "embedding_model": model_name(),
    }
    return render(request, "semantic_search/search.html", context)