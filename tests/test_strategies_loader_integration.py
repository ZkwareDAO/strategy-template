"""
策略配置加载器集成测试

使用实际配置文件测试 StrategiesLoader 的功能。
"""

import pytest
from pathlib import Path

from strategy_core.utils.strategies_loader import (
    StrategiesLoader,
    StrategyInstance,
)


# =============================================================================
# 使用实际配置文件的测试
# =============================================================================

class TestWithActualConfig:
    """使用实际配置文件的集成测试"""

    @pytest.fixture
    def actual_config_path(self) -> str:
        """返回实际配置文件路径"""
        return "config/strategies.yaml"

    def test_load_actual_config(self, actual_config_path: str):
        """测试加载实际配置文件"""
        loader = StrategiesLoader(config_path=actual_config_path)

        # 应该成功加载
        result = loader.load()
        assert result is loader  # 返回 self

    def test_actual_config_has_strategies(self, tmp_path):
        """测试登记表能展开出策略实例。

        模板的 config/strategies.yaml 默认空登记（例策略处于注释状态），
        故用临时登记表保证前提；overrides 取仓库自带的 BTCUSDT 示例。
        """
        registry = tmp_path / "strategies.yaml"
        registry.write_text(
            "strategies:\n"
            "  example_ma_cross:\n"
            "    trading_mode: \"paper_trading\"\n"
            "    symbols: [BTCUSDT]\n",
            encoding="utf-8",
        )
        loader = StrategiesLoader(config_path=str(registry))
        loader.load()

        instances = loader.expand_strategies()

        # 应该有多个策略实例
        assert len(instances) > 0

    def test_actual_config_backtest_settings(self, actual_config_path: str):
        """测试简化配置不再包含回测设置"""
        loader = StrategiesLoader(config_path=actual_config_path)
        loader.load()

        # 简化配置格式：回测配置已移到 backtest/config/main.yaml
        # StrategiesLoader 不再处理回测配置
        assert not hasattr(loader, 'backtest_config')





    def test_actual_config_symbols_uppercase(self, tmp_path):
        """测试所有 symbol 都是大写"""
        registry = tmp_path / "strategies.yaml"
        registry.write_text(
            "strategies:\n"
            "  example_ma_cross:\n"
            "    trading_mode: \"paper_trading\"\n"
            "    symbols: [BTCUSDT]\n",
            encoding="utf-8",
        )
        loader = StrategiesLoader(config_path=str(registry))
        loader.load()

        instances = loader.expand_strategies()

        assert len(instances) > 0
        for instance in instances:
            assert instance.symbol == instance.symbol.upper()


# =============================================================================
# 配置路径验证测试
# =============================================================================

class TestConfigPathValidation:
    """测试配置路径生成"""


    def test_config_path_special_symbols(self, tmp_path):
        """测试 per-symbol overrides 路径生成"""
        registry = tmp_path / "strategies.yaml"
        registry.write_text(
            "strategies:\n"
            "  example_ma_cross:\n"
            "    trading_mode: \"paper_trading\"\n"
            "    symbols: [BTCUSDT]\n",
            encoding="utf-8",
        )
        loader = StrategiesLoader(config_path=str(registry))
        loader.load()

        # 路径规则：strategies/<name>/overrides/<SYMBOL>.yaml
        instance = loader.get_strategy_by_name_symbol("example_ma_cross", "BTCUSDT")
        assert instance is not None
        assert instance.config_path.endswith(
            "strategies/example_ma_cross/overrides/BTCUSDT.yaml"
        )
