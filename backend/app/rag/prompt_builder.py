def build_context(matches):
    context_parts = []
    url_to_source = {}
    source_counter = 1

    for i, match in enumerate(matches):
        meta = match["metadata"]
        url = meta.get("url", "")

        # source_block = f"""
        #     [Source {i+1}]
        #     Title: {meta.get('title', '')}
        #     Question: {meta.get('question', '')}
        #     URL: {meta.get('url', '')}

        #     Content:
        #     {meta.get('text', '')}
        # """
        if url not in url_to_source:
            url_to_source[url] = source_counter
            source_counter += 1
        source_number = url_to_source[url]
            
        source_block = f"""
            [Chunk {i + 1} | Source {source_number}]
            URL: {meta.get('url', '')}

            Content:
            {meta.get('text', '')}
        """.strip()
        context_parts.append(source_block.strip())

    return "\n\n---\n\n".join(context_parts)