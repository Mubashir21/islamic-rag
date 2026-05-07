def build_context(matches):
    if not matches:
        return ""

    # Group chunks by URL, preserving first-seen order
    url_to_source = {}
    source_counter = 1
    grouped = {}

    for match in matches:
        meta = match["metadata"]
        url = meta.get("url", "")

        if url not in url_to_source:
            url_to_source[url] = source_counter
            grouped[url] = []
            source_counter += 1

        grouped[url].append(meta.get("text", "").strip())

    # Build context blocks grouped by source
    context_parts = []
    for url, chunks in grouped.items():
        source_number = url_to_source[url]
        block = f"[Source {source_number}]\nURL: {url}\n\n"
        block += "\n\n---\n\n".join(f"Chunk:\n{chunk}" for chunk in chunks)
        context_parts.append(block)

    return "\n\n===\n\n".join(context_parts)
