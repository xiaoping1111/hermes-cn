"""描述符

【产品经理理解要点】
中继描述符。
- 验证功能：中继节点的描述符定义
- 关键场景：描述符解析、校验、序列化
- 业务影响：中继描述符格式错误

─────────────────────────────────────────────────────────────────────────
Descriptor <- PlatformEntry projection (relay Phase 0, Task 0.3).

Proves the CapabilityDescriptor is a projection of the existing PlatformEntry,
not a parallel concept: the entry's label/limit/emoji/hint/pii fields carry
straight through."""

from gateway.platform_registry import PlatformEntry
from gateway.relay.descriptor import CONTRACT_VERSION, CapabilityDescriptor


def _entry(**overrides) -> PlatformEntry:
    base = dict(
        name="telegram",
        label="Telegram",
        adapter_factory=lambda cfg: None,
        check_fn=lambda: True,
        max_message_length=4096,
        pii_safe=False,
        emoji="\u2708\ufe0f",
        platform_hint="You are on Telegram.",
    )
    base.update(overrides)
    return PlatformEntry(**base)


def test_projection_carries_platform_entry_fields():
    d = CapabilityDescriptor.from_platform_entry(_entry(), len_unit="utf16")
    assert d.contract_version == CONTRACT_VERSION
    assert d.platform == "telegram"
    assert d.label == "Telegram"
    assert d.max_message_length == 4096
    assert d.emoji == "\u2708\ufe0f"
    assert d.platform_hint == "You are on Telegram."
    assert d.pii_safe is False
    assert d.len_unit == "utf16"


