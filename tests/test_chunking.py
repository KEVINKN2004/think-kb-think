from app.core.chunking import chunk_text


def test_short_text_returns_single_chunk():
    text = "This is a short document."
    chunks = chunk_text(text, chunk_size = 800, overlap = 100)
    assert len(chunks) == 1
    assert chunks[0] == text

def test_long_text_splits_into_multiple_chunks():
    text = "a" * 2000
    chunks = chunk_text(text, chunk_size = 800, overlap = 100)
    assert len(chunks) > 1

def test_chunks_respect_max_size():
    text = "a" * 2000
    chunks = chunk_text(text, chunk_size = 800, overlap = 100)
    assert all(len(c) <= 800 for c in chunks)

def test_chunks_overlap():
    text = "".join(str(i % 10) for i in range(2000))
    chunks = chunk_text(text, chunk_size = 800, overlap = 100)
    assert chunks[0][-100:] == chunks[1][:100]

def test_empty_text_returns_no_chunks():
    assert chunk_text("", chunk_size = 800, overlap = 100) == []

def test_whitespace_only_returns_no_chunks():
    assert chunk_text("   \n  ", chunk_size = 800, overlap = 100) == []

def test_full_text_is_preserved_across_chunks():
    text = "b" * 1500
    chunks = chunk_text(text, chunk_size = 800, overlap = 100)
    reassembled = chunks[0] + "".join(c[100:] for c in chunks[1:])
    assert reassembled == text