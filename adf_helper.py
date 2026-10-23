def text_to_adf(text):
    paragraphs = []
    for line in text.split("\n"):
        line = line.strip()
        if not line:
            continue
        if line.startswith("### "):
            paragraphs.append({
                "type": "heading",
                "attrs": {"level": 3},
                "content": [{"type": "text", "text": line[4:]}]
            })
        elif line.startswith("## "):
            paragraphs.append({
                "type": "heading",
                "attrs": {"level": 2},
                "content": [{"type": "text", "text": line[3:]}]
            })
        elif line.startswith("- ") or line.startswith("* "):
            paragraphs.append({
                "type": "bulletList",
                "content": [
                    {
                        "type": "listItem",
                        "content": [
                            {
                                "type": "paragraph",
                                "content": [{"type": "text", "text": line[2:]}]
                            }
                        ]
                    }
                ]
            })
        else:
            paragraphs.append({
                "type": "paragraph",
                "content": [{"type": "text", "text": line}]
            })
    return {
        "type": "doc",
        "version": 1,
        "content": paragraphs if paragraphs else [{"type": "paragraph", "content": [{"type": "text", "text": ""}]}]
    }
