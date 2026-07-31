"""测试 - toolset distributions

【产品经理理解要点】
功能验证中的toolset distributions验证。
- 验证功能：toolset distributions功能正确性验证
- 关键场景：核心逻辑、边界条件、错误处理
- 业务影响：toolset distributions功能异常或存在安全隐患

─────────────────────────────────────────────────────────────────────────
Tests for toolset_distributions.py — distribution CRUD, sampling, validation.
"""

import pytest

from toolset_distributions import (
    DISTRIBUTIONS,
    get_distribution,
    list_distributions,
    sample_toolsets_from_distribution,
    validate_distribution,
)


class TestGetDistribution:
    def test_known_distribution(self):
        dist = get_distribution("default")
        assert dist is not None
        assert "description" in dist
        assert "toolsets" in dist




class TestListDistributions:
    def test_returns_copy(self):
        d1 = list_distributions()
        d2 = list_distributions()
        assert d1 is not d2
        assert d1 == d2



class TestValidateDistribution:
    def test_valid(self):
        assert validate_distribution("default") is True
        assert validate_distribution("research") is True



class TestSampleToolsetsFromDistribution:


    def test_minimal_returns_web_only(self):
        result = sample_toolsets_from_distribution("minimal")
        assert "web" in result

    def test_returns_list_of_strings(self):
        result = sample_toolsets_from_distribution("balanced")
        assert isinstance(result, list)
        for item in result:
            assert isinstance(item, str)



class TestDistributionStructure:
    def test_all_have_required_keys(self):
        for name, dist in DISTRIBUTIONS.items():
            assert "description" in dist, f"{name} missing description"
            assert "toolsets" in dist, f"{name} missing toolsets"
            assert isinstance(dist["toolsets"], dict), f"{name} toolsets not a dict"

    def test_probabilities_are_valid_range(self):
        for name, dist in DISTRIBUTIONS.items():
            for ts_name, prob in dist["toolsets"].items():
                assert 0 < prob <= 100, f"{name}.{ts_name} has invalid probability {prob}"

