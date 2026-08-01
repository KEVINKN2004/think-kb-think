from dataclasses import dataclass, field

@dataclass
class EvalCase:
    question: str
    expected_document: str | None
    required_facts: list[str] = field(default_factory = list)
    should_answer: bool = True
    notes: str = ""

CASES: list[EvalCase] = [
    # --- Idea Validation ---
    EvalCase(
        question = "What percentage of users saying they'd be very disappointed indicates product/market fit?",
        expected_document = "idea_validation",
        required_facts = ["40"],
    ),
    EvalCase(
        question = "How many customer interviews should I do before drawing conclusions?",
        expected_document = "idea_validation",
        required_facts = ["10", "20"],
    ),
    EvalCase(
        question = "Why are waitlist signups a weak signal of demand?",
        expected_document = "idea_validation",
        required_facts = ["email"],
        notes = "Tests retrieval of a specific bullet inside a longer list.",
    ),
    EvalCase(
        question = "What's the difference between problem/solution fit and product/market fit?",
        expected_document = "idea_validation",
        required_facts = ["problem", "market"],
    ),
    EvalCase(
        question = "What segment should I do the interviews in before deciding on what problem to solve?",
        expected_document = "idea_validation",
        required_facts = ["single", "narrowly defined"]
    ),

    # --- Market Sizing ---
    EvalCase(
        question = "What do TAM, SAM, and SOM stand for?",
        expected_document = "market_sizing",
        required_facts = ["total addressable", "serviceable"],
    ),
    EvalCase(
        question = "How do I calculate market size bottom-up?",
        expected_document = "market_sizing",
        required_facts = ["customers", "revenue per customer"],
    ),
    EvalCase(
        question = "How large does a TAM need to be for venture funding?",
        expected_document = "market_sizing",
        required_facts = ["1 billion"],
    ),
    EvalCase(
        question = "Why is saying we only need one percent of the market a red flag?",
        expected_document = "market_sizing",
        required_facts = ["top-down"],
        notes = "Question phrasing differs substantially from corpus wording.",
    ),
    EvalCase(
        question = "What do investors prefer in terms of sizing and why?",
        expected_document = "market_sizing",
        required_facts = ["bottom-up", "inspectable"]
    ),

    # --- Co-Founder Decisions ---
    EvalCase(
        question = "What is the standard founder vesting schedule?",
        expected_document = "cofounder_decisions",
        required_facts = ["four-year", "cliff"],
    ),
    EvalCase(
        question = "How long do I have to file an 83(b) election?",
        expected_document = "cofounder_decisions",
        required_facts = ["30 days"],
        notes = "Fact sits deep in the document. Tests chunk boundary handling.",
    ),
    EvalCase(
        question = "What's the difference between single-trigger and double-trigger acceleration?",
        expected_document = "cofounder_decisions",
        required_facts = ["change of control", "terminated"],
    ),
    EvalCase(
        question = "What fraction of startup failures involve co-founder conflict?",
        expected_document = "cofounder_decisions",
        required_facts = ["65"],
    ),
    EvalCase(
        question = "What should go into a written founder agreement?",
        expected_document = "cofounder_decisions",
        required_facts = ["equity", "roles"],
        notes = "Multi-chunk: the agreement checklist likely spans a boundary.",
    ),
    EvalCase(
        question = "Why do equal splits or uneven splits?",
        expected_document = "cofounder_decisions",
        required_facts = ["comparable commitment", "differences in contribution"],
    ),

    # ---Fundraising Stages ---
    EvalCase(
        question = "What percentage of dilution is typical in a seed round?",
        expected_document = "fundraising_stages",
        required_facts = ["15", "25"],
    ),
    EvalCase(
        question = "How much do companies typically raise at pre-seed?",
        expected_document = "fundraising_stages",
        required_facts = ["500,000", "2 million"],
    ),
    EvalCase(
        question = "What ARR do investors expect at Series A?",
        expected_document = "fundraising_stages",
        required_facts = ["1 million", "2 million"],
    ),
    EvalCase(
        question = "What's the difference between a SAFE and a convertible note?",
        expected_document = "fundraising_stages",
        required_facts = ["interest", "maturity"],
    ),
    EvalCase(
        question = "What is the option pool shuffle and why does it matter?",
        expected_document = "fundraising_stages",
        required_facts = ["pre-money", "dilution"],
    ),
    EvalCase(
        question = "How big is a typical employee option pool?",
        expected_document = "fundraising_stages",
        required_facts = ["10", "20"],
    ),
    EvalCase(
        question = "What are the expected growth expectations for enterprise software?",
        expected_document = "fundraising_stages",
        required_facts = ["triple", "double"],
    ),

    # --- Revenue Models ---
    EvalCase(
        question = "What LTV to CAC ratio should a SaaS business target?",
        expected_document = "revenue_models",
        required_facts = ["3"],
    ),
    EvalCase(
        question = "What's a typical freemium free-to-paid conversion rate?",
        expected_document = "revenue_models",
        required_facts = ["2", "5"],
    ),
    EvalCase(
        question = "What gross margin should a software company have?",
        expected_document = "revenue_models",
        required_facts = ["70", "80"],
    ),
    EvalCase(
        question = "What take rate do marketplaces usually charge?",
        expected_document = "revenue_models",
        required_facts = ["15", "30"],
    ),
    EvalCase(
        question = "How does churn differ between consumer and B2B subscriptions?",
        expected_document = "revenue_models",
        required_facts = ["5", "10", "1"],
        notes = "Requires comparing two figures from the same passage.",
    ),
    EvalCase(
        question = "What does net revenue retention above 100 percent mean?",
        expected_document = "revenue_models",
        required_facts = ["expansion", "churn"],
    ),
    EvalCase(
        question = "How do consumer businesses win?",
        expected_document = "revenue_models",
        required_facts = ["distribution", "virality"],
    ),

    # --- Early GTM ---
    EvalCase(
        question = "How many customers should founders close before hiring a salesperson?",
        expected_document = "early_gtm",
        required_facts = ["10", "20"],
    ),
    EvalCase(
        question = "What is an ideal customer profile and how narrow should it be?",
        expected_document = "early_gtm",
        required_facts = ["ICP", "narrow"],
    ),
    EvalCase(
        question = "Should I charge design partners or give them the product free?",
        expected_document = "early_gtm",
        required_facts = ["charge"],
    ),
    EvalCase(
        question = "How long does content and SEO take to produce meaningful traffic?",
        expected_document = "early_gtm",
        required_facts = ["6", "12"],
    ),
    EvalCase(
        question = "What is a workable structure for early positioning?",
        expected_document = "early_gtm",
        required_facts = ["workable", "specific customer"]
    ),

    # --- Hiring Process ---
    EvalCase(
        question = "Should my first hires be generalists or specialists?",
        expected_document = "hiring_process",
        required_facts = ["generalists"],
    ),
    EvalCase(
        question = "How much equity should the first employee get?",
        expected_document = "hiring_process",
        required_facts = ["1", "2"],
    ),
    EvalCase(
        question = "When should I use a contractor instead of hiring an employee?",
        expected_document = "hiring_process",
        required_facts = ["bounded", "core"],
        notes = "Multi-chunk: contractor and employee criteria may split.",
    ),
    EvalCase(
        question = "How long should a paid work trial be?",
        expected_document = "hiring_process",
        required_facts = ["4", "8"],
    ),
    EvalCase(
        question = "When is the right time to hire a manager?",
        expected_document = "hiring_process",
        required_facts = ["five", "seven"],
    ),
    EvalCase(
        question = "Why does an employee joining a Series B startup accept less equity?",
        expected_document = "hiring_process",
        required_facts = ["Series B", "shares"],
    ),

    # --- Unanswerable: Completely outside collection ---
    EvalCase(
        question = "What is the capital of Mongolia?",
        expected_document = None,
        should_answer = False,
        notes = "Totally unrelated. Baseline refusal test.",
    ),
    EvalCase(
        question = "How do I optimize a PostgreSQL query plan?",
        expected_document = None,
        should_answer = False,
        notes = "Technical, adjacent to startups but absent from corpus.",
    ),

    # --- Unanswerable: Plausible near-miss edge cases ---
        EvalCase(
        question = "How do I calculate my startup's runway and burn multiple?",
        expected_document = None,
        should_answer = False,
        notes = "Deliberately removed from corpus. Hardest refusal case. Tests heavy vocabulary overlap with revenue_models and fundraising_stages.",
    ),
    EvalCase(
        question = "What are the standard terms in a Series C term sheet?",
        expected_document = None,
        should_answer = False,
        notes = "Collection stops at Series A. Tests whether it extrapolates beyond sources.",
    ),
    EvalCase(
        question = "Which states have the most favorable startup tax incentives?",
        expected_document = None,
        should_answer = False,
        notes = "Startup-adjacent, no coverage. Tests topical-similarity false positives.",
    ),
    EvalCase(
        question = "How should I structure an employee stock option plan for international contractors?",
        expected_document = None,
        should_answer = False,
        notes = "Corpus covers options and contractors separately but not this intersection. Tests for plausible-sounding synthesis.",
    ),
]