from mcp_marketing_suite.tools import (
    GenerateAds,
    GenerateCRMSequences,
    GenerateSEOPlan,
    GenerateStrategy,
    ScoreCopyQuality,
)


def test_generate_strategy():
    tool = GenerateStrategy()
    result = tool({"product": "Acme", "audience": "CMOs", "brand": "Direct", "goals": ["ROI"]})
    assert "value_proposition" in result.model_dump()


def test_generate_ads():
    tool = GenerateAds()
    payload = {
        "product": "Acme",
        "audience": "CMOs",
        "brand": "Direct",
        "channels": ["google", "meta", "linkedin"],
        "offers": ["demo"],
    }
    result = tool(payload)
    assert result.google


def test_generate_seo_plan():
    tool = GenerateSEOPlan()
    result = tool({"product": "Acme", "audience": "CMOs", "brand": "Direct"})
    assert result.clusters


def test_generate_crm_sequences():
    tool = GenerateCRMSequences()
    result = tool({"product": "Acme", "audience": "CMOs", "brand": "Direct", "channels": ["email"]})
    assert result.sequences


def test_score_copy_quality():
    tool = ScoreCopyQuality()
    result = tool({"copy": "Teste de copy"})
    assert 0 <= result.score <= 100
