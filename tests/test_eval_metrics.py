from app.core.retrieval import RetrievedChunk
from evals.metrics import (
    citations_present,
    fact_coverage,
    hit_at_k,
    looks_like_refusal,
    reciprocal_rank,
)


def _result(document_title: str, similarity: float = 0.7) -> RetrievedChunk:
    """Build a minimal RetrievedChunk for testing."""
    return RetrievedChunk(
        chunk_id=1,
        document_id=1,
        document_title=document_title,
        chunk_text="some text",
        similarity=similarity,
    )

# --- hit_at_k ---

def test_hit_at_k_true_when_expected_document_present():
    results = [_result("market_sizing"), _result("fundraising_stages")]
    assert hit_at_k(results, "fundraising_stages") is True

def test_hit_at_k_false_when_expected_document_absent():
    results = [_result("market_sizing"), _result("early_gtm")]
    assert hit_at_k(results, "revenue_models") is False

def test_hit_at_k_false_on_empty_results():
    assert hit_at_k([], "market_sizing") is False

# --- reciprocal_rank ---

def test_reciprocal_rank_first_position_is_one():
    results = [_result("target"), _result("other")]
    assert reciprocal_rank(results, "target") == 1.0

def test_reciprocal_rank_second_position_is_one_half():
    results = [_result("other"), _result("target")]
    assert reciprocal_rank(results, "target") == 0.5

def test_reciprocal_rank_third_position_is_one_third():
    results = [_result("a"), _result("b"), _result("target")]
    assert round(reciprocal_rank(results, "target"), 3) == 0.333

def test_reciprocal_rank_absent_is_zero():
    assert reciprocal_rank([_result("a"), _result("b")], "target") == 0.0

def test_reciprocal_rank_empty_results_is_zero():
    assert reciprocal_rank([], "target") == 0.0

def test_reciprocal_rank_uses_first_occurrence():
    """Two chunks from the same document should score by the earliest position."""
    results = [_result("other"), _result("target"), _result("target")]
    assert reciprocal_rank(results, "target") == 0.5

# --- fact_coverage ---

def test_fact_coverage_all_facts_found():
    answer = "Seed dilution is typically 15 to 25 percent."
    assert fact_coverage(answer, ["15", "25"]) == 1.0

def test_fact_coverage_partial():
    answer = "Seed dilution is around 15 percent."
    assert fact_coverage(answer, ["15", "25"]) == 0.5

def test_fact_coverage_none_found():
    assert fact_coverage("No relevant numbers here.", ["15", "25"]) == 0.0

def test_fact_coverage_is_case_insensitive():
    answer = "You must file the 83(B) ELECTION within 30 DAYS."
    assert fact_coverage(answer, ["83(b)", "30 days"]) == 1.0

def test_fact_coverage_empty_requirements_is_full():
    assert fact_coverage("anything at all", []) == 1.0

def test_fact_coverage_empty_answer_is_zero():
    assert fact_coverage("", ["15"]) == 0.0

# --- looks_like_refusal ---

def test_looks_like_refusal_detects_no_information_phrase():
    answer = "I don't have information about that in the knowledge base."
    assert looks_like_refusal(answer) is True

def test_looks_like_refusal_false_for_real_answer():
    answer = "Seed rounds typically involve 15 to 25 percent dilution [1]."
    assert looks_like_refusal(answer) is False

def test_looks_like_refusal_is_case_insensitive():
    assert looks_like_refusal("I DON'T HAVE INFORMATION on that topic.") is True

def test_looks_like_refusal_false_on_empty_answer():
    assert looks_like_refusal("") is False
    
def test_looks_like_refusal_detects_do_not_contain():
    answer = "The sources provided do not contain information about that topic."
    assert looks_like_refusal(answer) is True

# --- citations_present ---

def test_citations_present_detects_single_bracket():
    assert citations_present("As shown in [1], runway matters.", 2) is True

def test_citations_present_detects_later_source_number():
    assert citations_present("According to [3], take rates vary.", 3) is True

def test_citations_absent_when_no_brackets():
    assert citations_present("Take rates vary by marketplace.", 2) is False

def test_citations_present_true_when_no_sources_to_cite():
    """A refusal has nothing to cite, so it should not be penalized."""
    assert citations_present("I don't have information about that.", 0) is True
