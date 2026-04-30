def build_context(matches):
    context_parts = []

    for i, match in enumerate(matches):
        meta = match["metadata"]

        source_block = f"""
            [Source {i+1}]
            Title: {meta.get('title', '')}
            Question: {meta.get('question', '')}
            URL: {meta.get('url', '')}

            Content:
            {meta.get('text', '')}
        """
        context_parts.append(source_block.strip())

    return "\n\n---\n\n".join(context_parts)