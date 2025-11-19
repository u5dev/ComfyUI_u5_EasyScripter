# -*- coding: utf-8 -*-
"""
ループ制御関数
サブグラフループ実行機能を提供
"""

try:
    from ..locales import get_message
except ImportError:
    from locales import get_message

def builtin_loop_subgraph(count, channel="RETURN1", engine=None, locale='ja'):
    """
    サブグラフループ実行を設定

    この関数を呼び出すと、EasyScripterの後続ノード(サブグラフ)が
    指定回数繰り返し実行されます。

    Args:
        count (int or str): 繰り返し回数(1-100の範囲、範囲外は自動調整)
            - 整数または整数文字列: そのまま使用
            - 小数点文字列: float変換後にint変換(切り捨て)
            例: "1.3" → 1, "99.9" → 99, "0.5" → 0 → 1(クランプ)
        channel (str): 出力チャネル
            - "RETURN1": RETURN1の出力を使用
            - "RETURN2": RETURN2の出力を使用
            - "RELAY": relay_outputを使用
            - None または "AUTO": 自動選択(接続されている全チャネルに適用)
        engine (ScriptEngine): スクリプトエンジンインスタンス(自動渡し)

    Returns:
        int: 設定した繰り返し回数(クランプ後の値)

    Raises:
        RuntimeError: engineがNoneの場合
        ValueError: countが数値変換不可能な場合、またはchannelが不正な場合

    使用例:
        ```vba
        ' RETURN1を5回繰り返す
        RETURN1 = VAL1 * 2
        LOOP_SUBGRAPH(5, "RETURN1")
        ```

        ```vba
        ' relay_outputを3回繰り返す(画像処理パイプライン等)
        LOOP_SUBGRAPH(3, "relay")
        ```

        ```vba
        ' 自動チャネル選択(接続されている全チャネルに適用)
        RETURN1 = "prompt text"
        RETURN2 = 512
        LOOP_SUBGRAPH(5)  # RETURN1とRETURN2両方に5回ずつ設定
        ```

        ```vba
        ' 範囲外の値は自動調整される
        LOOP_SUBGRAPH(0, "RETURN1")    # 1に調整
        LOOP_SUBGRAPH(150, "RETURN1")  # 100に調整
        ```

        ```vba
        ' 小数点文字列も受け入れ(切り捨て)
        LOOP_SUBGRAPH("1.3", "RETURN1")   # 1回に変換
        LOOP_SUBGRAPH("99.9", "RETURN1")  # 99回に変換
        ```

        ```vba
        ' 複数チャネル個別設定(同じサブグラフなら統合実行)
        LOOP_SUBGRAPH(1, "RETURN1")
        LOOP_SUBGRAPH(2, "RETURN2")
        # → 同じサブグラフに接続されている場合、合計3回実行
        ```
    """
    # 🚨 CRITICAL FIX: 引数順序の自動検出と再配置
    # script_engine.pyは func(self, *args, locale=locale) で呼び出すため、
    # 第1引数にScriptEngineオブジェクトが渡される可能性がある

    # 第1引数がScriptEngineインスタンスか検出(インポート不要の型チェック)
    # type(count).__name__ == 'ScriptEngine' で判定(動的インポート禁止ルール対応)
    if hasattr(count, '__class__') and type(count).__name__ == 'ScriptEngine':
        # 引数が1つずれている: (engine, count, channel) → 再配置
        # 呼び出し: func(self, 2, "RETURN2", locale='ja')
        # マッピング: count=self, channel=2, engine="RETURN2", locale='ja'(keyword arg)

        # 一時変数に保存(変数上書きを防ぐ)
        temp_engine = count       # ScriptEngineインスタンスを保存
        temp_count = channel      # count値を保存(元のchannelパラメータ位置)
        temp_channel = engine     # channel値を保存(元のengineパラメータ位置)

        # 正しい順序に再配置
        engine = temp_engine
        count = temp_count
        channel = temp_channel if temp_channel is not None else "RETURN1"
        # locale引数はキーワード引数として渡されるため再配置不要

        # デバッグログ
        print(get_message('loop_arg_reorder_detected', locale, count, channel))
    
    if engine is None:
        raise RuntimeError(get_message('loop_engine_required', locale))

    # 回数の検証(小数点文字列対応)
    try:
        # float経由で変換→int変換(小数点切り捨て)
        count = int(float(count))
    except (ValueError, TypeError):
        raise ValueError(get_message('loop_count_must_be_integer', locale, count))

    # 範囲外の値を自動的にクランプ(1-100の範囲に収める)
    original_count = count
    if count < 1:
        count = 1
        print(get_message('loop_count_clamped_to_min', locale, original_count))
    elif count > 100:
        count = 100
        print(get_message('loop_count_clamped_to_max', locale, original_count))

    # チャネルの検証
    # Noneの場合はAUTOに変換(後方互換性のため)
    if channel is None:
        channel = "AUTO"
    else:
        channel = str(channel).upper()

    valid_channels = ["RETURN1", "RETURN2", "RELAY", "AUTO"]
    if channel not in valid_channels:
        raise ValueError(get_message('loop_invalid_channel', locale, valid_channels, channel))

    # チャネル別にループ設定を保存(後勝ち優先)
    if channel == "AUTO":
        # AUTO設定: 実行時に接続されている全チャネルに展開
        engine.loop_config["_AUTO_"] = {
            "enabled": True,
            "count": count,
            "needs_detection": True  # scripter_node.pyで接続先を自動検出
        }
        print(get_message('loop_set_auto_channel', locale, count))
    else:
        # 通常のチャネル指定: チャネル別に保存
        engine.loop_config[channel] = {
            "enabled": True,
            "count": count,
            "current_iteration": 0
        }
        print(get_message('loop_set_specific_channel', locale, channel, count))

    return count
