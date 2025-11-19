# -*- coding: utf-8 -*-
"""
数学関数と三角関数のモジュール
Math and trigonometric functions module
"""

from typing import Any
import math
import random
# グローバルインポート（CLAUDE.md動的インポート禁止ルールに準拠）
# 相対インポートを試し、失敗時はフォールバック（テスト環境対応）
try:
    from ..locales import get_message
except ImportError:
    try:
        from locales import get_message
    except ImportError:
        # localesがない環境用フォールバック
        def get_message(key, locale='ja'):
            return key

class MathFunctions:
    """数学・三角関数のクラス"""

    @staticmethod
    def ABS(value: Any) -> float:
        """
        絶対値を返す

        Args:
            value: 数値または数値に変換可能な値

        Returns:
            絶対値（float）

        Examples:
            ABS(-4.3) → 4.3
            ABS(5) → 5.0
            ABS("-10") → 10.0
        """
        try:
            num_value = float(value)
            return abs(num_value)
        except (TypeError, ValueError):
            # 数値に変換できない場合は0を返す（VBAの動作に準拠）
            return 0.0

    @staticmethod
    def INT(value: Any) -> float:
        """
        整数部分を返す（小数点以下切り捨て）

        Args:
            value: 数値または数値に変換可能な値

        Returns:
            整数部分（float形式）
        """
        try:
            num_value = float(value)
            if num_value >= 0:
                return math.floor(num_value)
            else:
                return math.ceil(num_value)
        except (TypeError, ValueError):
            return 0.0

    # ROUND関数は base_functions.py に移動

    @staticmethod
    def SQRT(value: Any) -> float:
        """
        平方根を返す

        Args:
            value: 数値または数値に変換可能な値

        Returns:
            平方根（負の値の場合はエラー）
        """
        try:
            num_value = float(value)
            if num_value < 0:
                raise ValueError(get_message('error_sqrt_negative', 'ja'))
            return math.sqrt(num_value)
        except (TypeError, ValueError) as e:
            if "sqrt" in str(e).lower():
                raise
            return 0.0

    @staticmethod
    def MIN(*args) -> float:
        """
        最小値を返す

        Args:
            *args: 複数の数値

        Returns:
            最小値
        """
        if not args:
            return 0.0
        try:
            numeric_values = [float(arg) for arg in args]
            return min(numeric_values)
        except (TypeError, ValueError):
            return 0.0

    @staticmethod
    def MAX(*args) -> float:
        """
        最大値を返す

        Args:
            *args: 複数の数値

        Returns:
            最大値
        """
        if not args:
            return 0.0
        try:
            numeric_values = [float(arg) for arg in args]
            return max(numeric_values)
        except (TypeError, ValueError):
            return 0.0

    @staticmethod
    def SIN(value: Any) -> float:
        """
        サイン値を返す（ラジアン単位）

        Args:
            value: 角度（ラジアン）

        Returns:
            サイン値
        """
        try:
            num_value = float(value)
            return math.sin(num_value)
        except (TypeError, ValueError):
            return 0.0

    @staticmethod
    def COS(value: Any) -> float:
        """
        コサイン値を返す（ラジアン単位）

        Args:
            value: 角度（ラジアン）

        Returns:
            コサイン値
        """
        try:
            num_value = float(value)
            return math.cos(num_value)
        except (TypeError, ValueError):
            return 0.0

    @staticmethod
    def TAN(value: Any) -> float:
        """
        タンジェント値を返す（ラジアン単位）

        Args:
            value: 角度（ラジアン）

        Returns:
            タンジェント値
        """
        try:
            num_value = float(value)
            return math.tan(num_value)
        except (TypeError, ValueError):
            return 0.0

    @staticmethod
    def RADIANS(degrees: Any) -> float:
        """
        度をラジアンに変換

        Args:
            degrees: 角度（度単位）

        Returns:
            ラジアン値
        """
        try:
            deg_value = float(degrees)
            return math.radians(deg_value)
        except (TypeError, ValueError):
            return 0.0

    @staticmethod
    def DEGREES(radians: Any) -> float:
        """
        ラジアンを度に変換

        Args:
            radians: 角度（ラジアン単位）

        Returns:
            度数
        """
        try:
            rad_value = float(radians)
            return math.degrees(rad_value)
        except (TypeError, ValueError):
            return 0.0

    @staticmethod
    def AVG(*args) -> float:
        """
        平均値を返す

        Args:
            *args: 複数の数値

        Returns:
            平均値
        """
        if not args:
            return 0.0
        try:
            numeric_values = [float(arg) for arg in args]
            return sum(numeric_values) / len(numeric_values)
        except (TypeError, ValueError, ZeroDivisionError):
            return 0.0

    @staticmethod
    def SUM(*args) -> float:
        """
        合計値を返す

        Args:
            *args: 複数の数値

        Returns:
            合計値
        """
        if not args:
            return 0.0
        try:
            numeric_values = [float(arg) for arg in args]
            return sum(numeric_values)
        except (TypeError, ValueError):
            return 0.0

    @staticmethod
    def POW(base: Any, exponent: Any) -> float:
        """
        べき乗を計算

        Args:
            base: 基数
            exponent: 指数

        Returns:
            base^exponentの値
        """
        try:
            base_value = float(base)
            exp_value = float(exponent)
            return math.pow(base_value, exp_value)
        except (TypeError, ValueError):
            return 0.0

    @staticmethod
    def LOG(value: Any, base: Any = None) -> float:
        """
        対数を計算（VBA互換：デフォルトは自然対数）

        Args:
            value: 真数
            base: 底（省略時は自然対数）

        Returns:
            対数値
        """
        try:
            num_value = float(value)
            if num_value <= 0:
                raise ValueError(get_message('error_log_invalid_arg', 'ja'))

            # VBAのLOGはデフォルトで自然対数
            if base is None:
                return math.log(num_value)  # 自然対数
            else:
                base_value = float(base)
                if base_value <= 0 or base_value == 1:
                    raise ValueError(get_message('error_log_invalid_base', 'ja'))
                return math.log(num_value, base_value)
        except (TypeError, ValueError) as e:
            if "log" in str(e).lower():
                raise
            return 0.0

    @staticmethod
    def EXP(value: Any) -> float:
        """
        e^値を計算

        Args:
            value: 指数

        Returns:
            e^valueの値
        """
        try:
            num_value = float(value)
            return math.exp(num_value)
        except (TypeError, ValueError):
            return 0.0

    @staticmethod
    def FIX(value: Any) -> float:
        """
        整数部分を返す（ゼロ方向への切り捨て）

        Args:
            value: 数値

        Returns:
            整数部分（float形式）
        """
        try:
            num_value = float(value)
            return math.trunc(num_value)
        except (TypeError, ValueError):
            return 0.0

    @staticmethod
    def SGN(value: Any) -> float:
        """
        数値の符号を返す

        Args:
            value: 数値

        Returns:
            -1（負）、0（ゼロ）、1（正）
        """
        try:
            num_value = float(value)
            if num_value > 0:
                return 1.0
            elif num_value < 0:
                return -1.0
            else:
                return 0.0
        except (TypeError, ValueError):
            return 0.0

    @staticmethod
    def ASIN(value: Any) -> float:
        """
        アークサイン（逆正弦）を返す

        Args:
            value: -1から1の間の値

        Returns:
            アークサイン（ラジアン）
        """
        try:
            num_value = float(value)
            if num_value < -1 or num_value > 1:
                raise ValueError(get_message('error_asin_range', 'ja'))
            return math.asin(num_value)
        except (TypeError, ValueError) as e:
            if "asin" in str(e).lower():
                raise
            return 0.0

    @staticmethod
    def ACOS(value: Any) -> float:
        """
        アークコサイン（逆余弦）を返す

        Args:
            value: -1から1の間の値

        Returns:
            アークコサイン（ラジアン）
        """
        try:
            num_value = float(value)
            if num_value < -1 or num_value > 1:
                raise ValueError(get_message('error_acos_range', 'ja'))
            return math.acos(num_value)
        except (TypeError, ValueError) as e:
            if "acos" in str(e).lower():
                raise
            return 0.0

    @staticmethod
    def ATAN(value: Any) -> float:
        """
        アークタンジェント（逆正接）を返す

        Args:
            value: 数値

        Returns:
            アークタンジェント（ラジアン）
        """
        try:
            num_value = float(value)
            return math.atan(num_value)
        except (TypeError, ValueError):
            return 0.0

    @staticmethod
    def LOG10(value: Any) -> float:
        """
        常用対数（底10）を計算

        Args:
            value: 正の数値

        Returns:
            常用対数
        """
        try:
            num_value = float(value)
            if num_value <= 0:
                raise ValueError(get_message('error_log10_positive', 'ja'))
            return math.log10(num_value)
        except (TypeError, ValueError) as e:
            if "log10" in str(e).lower():
                raise
            return 0.0

    @staticmethod
    def CEILING(value: Any) -> float:
        """
        天井関数（切り上げ）

        Args:
            value: 数値

        Returns:
            切り上げた値
        """
        try:
            num_value = float(value)
            return math.ceil(num_value)
        except (TypeError, ValueError):
            return 0.0

    @staticmethod
    def FLOOR(value: Any) -> float:
        """
        床関数（切り下げ）

        Args:
            value: 数値

        Returns:
            切り下げた値
        """
        try:
            num_value = float(value)
            return math.floor(num_value)
        except (TypeError, ValueError):
            return 0.0

    @staticmethod
    def RAND(min_value: Any = 0, max_value: Any = 1) -> float:
        """
        Generate a random float between min_value and max_value (inclusive of min, exclusive of max)

        Args:
            min_value: Minimum value (default: 0)
            max_value: Maximum value (default: 1)

        Returns:
            Random float between min_value and max_value

        Examples:
            RAND() -> 0.0 to 1.0
            RAND(1, 10) -> 1.0 to 10.0
            RAND(0, 100) -> 0.0 to 100.0
        """
        try:
            min_val = float(min_value) if min_value is not None else 0.0
            max_val = float(max_value) if max_value is not None else 1.0

            # 引数が逆の場合は入れ替える
            if min_val > max_val:
                min_val, max_val = max_val, min_val

            return random.uniform(min_val, max_val)
        except (TypeError, ValueError):
            return random.random()  # デフォルトで0.0から1.0の乱数

    @staticmethod
    def RANDOMIZE(*args) -> float:
        """
        Configure the random-number seed (VBA Randomize equivalent)

        Args:
            *args: Optional arguments
                - no argument: seed with system entropy
                - one argument: use the provided seed value
                - two arguments: draw a seed between min and max

        Returns:
            The seed value that was set (float)
        """
        def _random_seed_from_range(min_value: float, max_value: float) -> int:
            if min_value > max_value:
                min_value, max_value = max_value, min_value
            generator = random.SystemRandom()
            return int(generator.uniform(min_value, max_value))

        try:
            if len(args) == 0:
                seed_value = _random_seed_from_range(0, 2 ** 31 - 1)
            elif len(args) == 1:
                arg = args[0]
                if arg is None or str(arg).strip() == "":
                    seed_value = _random_seed_from_range(0, 2 ** 31 - 1)
                else:
                    seed_value = int(float(arg))
            else:
                min_value = float(args[0])
                max_value = float(args[1])
                seed_value = _random_seed_from_range(min_value, max_value)
        except (TypeError, ValueError):
            seed_value = _random_seed_from_range(0, 2 ** 31 - 1)

        random.seed(seed_value)
        return float(seed_value)

    # エイリアス関数
    @staticmethod
    def RND(*args) -> float:
        """RANDのエイリアス"""
        if len(args) == 0:
            return MathFunctions.RAND()
        elif len(args) == 1:
            return MathFunctions.RAND(0, args[0])
        else:
            return MathFunctions.RAND(*args)

    @staticmethod
    def SQR(value: Any) -> float:
        """SQRTのエイリアス（VBA互換）"""
        return MathFunctions.SQRT(value)