# -*- coding: utf-8 -*-
"""
日付・時刻関数のモジュール
Date and time functions module
"""

from typing import Any
from datetime import datetime, timedelta
import re

class DateFunctions:
    """日付・時刻関数のクラス"""

    @staticmethod
    def NOW() -> str:
        """
        現在の日時を返す（VBA互換）

        Returns:
            現在の日時（文字列形式: "YYYY/MM/DD HH:MM:SS"）
        """
        return datetime.now().strftime("%Y/%m/%d %H:%M:%S")

    @staticmethod
    def DATE() -> str:
        """
        現在の日付を返す（VBA互換）

        Returns:
            現在の日付（文字列形式: "YYYY/MM/DD"）
        """
        return datetime.now().strftime("%Y/%m/%d")

    @staticmethod
    def TIME() -> str:
        """
        現在の時刻を返す（VBA互換）

        Returns:
            現在の時刻（文字列形式: "HH:MM:SS"）
        """
        return datetime.now().strftime("%H:%M:%S")

    @staticmethod
    def YEAR(*args) -> float:
        """
        日付から年を取得（VBA互換）

        Args:
            引数なし: 現在日時の年
            1引数: 日付文字列から年を抽出
            3引数: 年、月、日を指定して年を返す

        Returns:
            年（数値）
        """
        try:
            if len(args) == 0:
                # 引数なし：現在の年
                return float(datetime.now().year)
            elif len(args) == 1:
                # 1引数：日付文字列から年を抽出
                date_value = args[0]
                if date_value is None or str(date_value).strip() == "":
                    dt = datetime.now()
                else:
                    # 様々な日付形式をパース
                    date_str = str(date_value).strip()
                    # スラッシュまたはハイフン区切りをサポート
                    for fmt in ["%Y/%m/%d %H:%M:%S", "%Y/%m/%d", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d",
                               "%m/%d/%Y", "%d/%m/%Y", "%Y年%m月%d日"]:
                        try:
                            dt = datetime.strptime(date_str, fmt)
                            break
                        except ValueError:
                            continue
                    else:
                        # どのフォーマットでもパースできなかった場合
                        return float(datetime.now().year)
                return float(dt.year)
            elif len(args) == 3:
                # 3引数：年、月、日を指定して年を返す
                year = float(args[0])
                return year
            else:
                # その他の引数数はエラー
                return float(datetime.now().year)
        except:
            return float(datetime.now().year)

    @staticmethod
    def MONTH(*args) -> float:
        """
        日付から月を取得（VBA互換）

        Args:
            引数なし: 現在日時の月
            1引数: 日付文字列から月を抽出
            3引数: 年、月、日を指定して月を返す

        Returns:
            月（数値: 1-12）
        """
        try:
            if len(args) == 0:
                # 引数なし：現在の月
                return float(datetime.now().month)
            elif len(args) == 1:
                # 1引数：日付文字列から月を抽出
                date_value = args[0]
                if date_value is None or str(date_value).strip() == "":
                    dt = datetime.now()
                else:
                    # 様々な日付形式をパース
                    date_str = str(date_value).strip()
                    for fmt in ["%Y/%m/%d %H:%M:%S", "%Y/%m/%d", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d",
                               "%m/%d/%Y", "%d/%m/%Y", "%Y年%m月%d日"]:
                        try:
                            dt = datetime.strptime(date_str, fmt)
                            break
                        except ValueError:
                            continue
                    else:
                        return float(datetime.now().month)
                return float(dt.month)
            elif len(args) == 3:
                # 3引数：年、月、日を指定して月を返す
                month = float(args[1])
                return month
            else:
                # その他の引数数はエラー
                return float(datetime.now().month)
        except:
            return float(datetime.now().month)

    @staticmethod
    def DAY(*args) -> float:
        """
        日付から日を取得（VBA互換）

        Args:
            引数なし: 現在日時の日
            1引数: 日付文字列から日を抽出
            3引数: 年、月、日を指定して日を返す

        Returns:
            日（数値: 1-31）
        """
        try:
            if len(args) == 0:
                # 引数なし：現在の日
                return float(datetime.now().day)
            elif len(args) == 1:
                # 1引数：日付文字列から日を抽出
                date_value = args[0]
                if date_value is None or str(date_value).strip() == "":
                    dt = datetime.now()
                else:
                    # 様々な日付形式をパース
                    date_str = str(date_value).strip()
                    for fmt in ["%Y/%m/%d %H:%M:%S", "%Y/%m/%d", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d",
                           "%m/%d/%Y", "%d/%m/%Y", "%Y年%m月%d日"]:
                        try:
                            dt = datetime.strptime(date_str, fmt)
                            break
                        except ValueError:
                            continue
                    else:
                        return float(datetime.now().day)
                return float(dt.day)
            elif len(args) == 3:
                # 3引数：年、月、日を指定して日を返す
                day = float(args[2])
                return day
            else:
                # その他の引数数はエラー
                return float(datetime.now().day)
        except:
            return float(datetime.now().day)

    @staticmethod
    def HOUR(time_value: Any = None) -> float:
        """
        時刻から時を取得（VBA互換）

        Args:
            time_value: 時刻文字列または日時文字列、省略時は現在時刻

        Returns:
            時（数値: 0-23）
        """
        try:
            if time_value is None or str(time_value).strip() == "":
                dt = datetime.now()
            else:
                # 様々な時刻・日時形式をパース
                time_str = str(time_value).strip()
                for fmt in ["%H:%M:%S", "%H:%M", "%Y/%m/%d %H:%M:%S", "%Y-%m-%d %H:%M:%S"]:
                    try:
                        dt = datetime.strptime(time_str, fmt)
                        break
                    except ValueError:
                        continue
                else:
                    return float(datetime.now().hour)
            return float(dt.hour)
        except:
            return float(datetime.now().hour)

    @staticmethod
    def MINUTE(time_value: Any = None) -> float:
        """
        時刻から分を取得（VBA互換）

        Args:
            time_value: 時刻文字列または日時文字列、省略時は現在時刻

        Returns:
            分（数値: 0-59）
        """
        try:
            if time_value is None or str(time_value).strip() == "":
                dt = datetime.now()
            else:
                # 様々な時刻・日時形式をパース
                time_str = str(time_value).strip()
                for fmt in ["%H:%M:%S", "%H:%M", "%Y/%m/%d %H:%M:%S", "%Y-%m-%d %H:%M:%S"]:
                    try:
                        dt = datetime.strptime(time_str, fmt)
                        break
                    except ValueError:
                        continue
                else:
                    return float(datetime.now().minute)
            return float(dt.minute)
        except:
            return float(datetime.now().minute)

    @staticmethod
    def SECOND(time_value: Any = None) -> float:
        """
        時刻から秒を取得（VBA互換）

        Args:
            time_value: 時刻文字列または日時文字列、省略時は現在時刻

        Returns:
            秒（数値: 0-59）
        """
        try:
            if time_value is None or str(time_value).strip() == "":
                dt = datetime.now()
            else:
                # 様々な時刻・日時形式をパース
                time_str = str(time_value).strip()
                for fmt in ["%H:%M:%S", "%H:%M", "%Y/%m/%d %H:%M:%S", "%Y-%m-%d %H:%M:%S"]:
                    try:
                        dt = datetime.strptime(time_str, fmt)
                        break
                    except ValueError:
                        continue
                else:
                    # %H:%M形式の場合、秒は0
                    if ":" in time_str and time_str.count(":") == 1:
                        return 0.0
                    return float(datetime.now().second)
            return float(dt.second)
        except:
            return float(datetime.now().second)

    @staticmethod
    def WEEKDAY(date_value: Any = None, first_day_of_week: int = 1) -> float:
        """
        日付から曜日番号を取得（VBA互換）

        Args:
            date_value: 日付文字列または日時文字列、省略時は今日
            first_day_of_week: 週の最初の曜日（1=日曜、2=月曜）、デフォルトは1

        Returns:
            曜日番号（1=日曜、2=月曜、...、7=土曜）
        """
        try:
            if date_value is None or str(date_value).strip() == "":
                dt = datetime.now()
            else:
                # 様々な日付形式をパース
                date_str = str(date_value).strip()
                for fmt in ["%Y/%m/%d %H:%M:%S", "%Y/%m/%d", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d"]:
                    try:
                        dt = datetime.strptime(date_str, fmt)
                        break
                    except ValueError:
                        continue
                else:
                    dt = datetime.now()

            # Pythonのweekday()は月曜=0なので、VBAスタイル（日曜=1）に変換
            # Python: 0=月, 1=火, 2=水, 3=木, 4=金, 5=土, 6=日
            # VBA:    1=日, 2=月, 3=火, 4=水, 5=木, 6=金, 7=土
            python_weekday = dt.weekday()
            # 日曜日の場合
            if python_weekday == 6:
                return 1.0
            else:
                return float(python_weekday + 2)
        except:
            return 1.0  # エラー時は日曜日を返す

    @staticmethod
    def DATEADD(interval: str, number: Any, date_value: Any = None) -> str:
        """
        日付に指定した間隔を加算（VBA互換）

        Args:
            interval: 間隔の種類 ("yyyy", "q", "m", "d", "h", "n", "s")
            number: 加算する数値（負の値で減算）
            date_value: 基準日付（省略時は現在日時）

        Returns:
            計算後の日付文字列
        """
        try:
            # 基準日付のパース
            if date_value is None or str(date_value).strip() == "":
                dt = datetime.now()
            else:
                date_str = str(date_value).strip()
                for fmt in ["%Y/%m/%d %H:%M:%S", "%Y/%m/%d", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d"]:
                    try:
                        dt = datetime.strptime(date_str, fmt)
                        break
                    except ValueError:
                        continue
                else:
                    dt = datetime.now()

            # 数値を取得
            try:
                num = int(float(number))
            except:
                num = 0

            # 間隔タイプに応じて計算
            interval_upper = str(interval).upper()
            if interval_upper in ["YYYY", "YY", "Y"]:
                # 年を加算
                dt = dt.replace(year=dt.year + num)
            elif interval_upper in ["Q", "QQ"]:
                # 四半期を加算（3ヶ月単位）
                months = num * 3
                new_month = dt.month + months
                years_to_add = (new_month - 1) // 12
                new_month = ((new_month - 1) % 12) + 1
                dt = dt.replace(year=dt.year + years_to_add, month=new_month)
            elif interval_upper in ["M", "MM"]:
                # 月を加算
                new_month = dt.month + num
                years_to_add = (new_month - 1) // 12
                new_month = ((new_month - 1) % 12) + 1
                dt = dt.replace(year=dt.year + years_to_add, month=new_month)
            elif interval_upper in ["D", "DD"]:
                # 日を加算
                dt = dt + timedelta(days=num)
            elif interval_upper in ["H", "HH"]:
                # 時間を加算
                dt = dt + timedelta(hours=num)
            elif interval_upper in ["N", "MI"]:
                # 分を加算
                dt = dt + timedelta(minutes=num)
            elif interval_upper in ["S", "SS"]:
                # 秒を加算
                dt = dt + timedelta(seconds=num)

            # 結果を返す
            return dt.strftime("%Y/%m/%d %H:%M:%S")
        except:
            return ""

    @staticmethod
    def DATEDIFF(interval: str, date1: Any, date2: Any = None) -> float:
        """
        2つの日付の差を計算（VBA互換）

        Args:
            interval: 間隔の種類 ("yyyy", "q", "m", "d", "h", "n", "s")
            date1: 開始日付
            date2: 終了日付（省略時は現在日時）

        Returns:
            日付間隔の数値（date2 - date1）
        """
        try:
            # 日付1のパース
            date1_str = str(date1).strip()
            dt1 = None
            for fmt in ["%Y/%m/%d %H:%M:%S", "%Y/%m/%d", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d"]:
                try:
                    dt1 = datetime.strptime(date1_str, fmt)
                    break
                except ValueError:
                    continue
            if dt1 is None:
                return 0.0

            # 日付2のパース
            if date2 is None or str(date2).strip() == "":
                dt2 = datetime.now()
            else:
                date2_str = str(date2).strip()
                dt2 = None
                for fmt in ["%Y/%m/%d %H:%M:%S", "%Y/%m/%d", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d"]:
                    try:
                        dt2 = datetime.strptime(date2_str, fmt)
                        break
                    except ValueError:
                        continue
                if dt2 is None:
                    dt2 = datetime.now()

            # 間隔タイプに応じて差を計算
            interval_upper = str(interval).upper()

            if interval_upper in ["YYYY", "YY", "Y"]:
                # 年の差
                return float(dt2.year - dt1.year)
            elif interval_upper in ["Q", "QQ"]:
                # 四半期の差
                q1 = (dt1.month - 1) // 3 + 1
                q2 = (dt2.month - 1) // 3 + 1
                return float((dt2.year - dt1.year) * 4 + (q2 - q1))
            elif interval_upper in ["M", "MM"]:
                # 月の差
                return float((dt2.year - dt1.year) * 12 + (dt2.month - dt1.month))
            elif interval_upper in ["D", "DD"]:
                # 日の差
                delta = dt2 - dt1
                return float(delta.days)
            elif interval_upper in ["H", "HH"]:
                # 時間の差
                delta = dt2 - dt1
                return float(delta.total_seconds() / 3600)
            elif interval_upper in ["N", "MI"]:
                # 分の差
                delta = dt2 - dt1
                return float(delta.total_seconds() / 60)
            elif interval_upper in ["S", "SS"]:
                # 秒の差
                delta = dt2 - dt1
                return float(delta.total_seconds())
            else:
                # 不明な間隔の場合は日数を返す
                delta = dt2 - dt1
                return float(delta.days)

        except:
            return 0.0

    @staticmethod
    def DATEVALUE(date_string: Any) -> str:
        """
        日付文字列を標準日付形式に変換

        Args:
            date_string: 日付を表す文字列

        Returns:
            標準形式の日付文字列（YYYY-MM-DD）
        """
        try:
            date_str = str(date_string)
            # 様々な形式を試す
            formats = [
                "%Y-%m-%d", "%Y/%m/%d", "%d/%m/%Y", "%m/%d/%Y",
                "%Y%m%d", "%d-%m-%Y", "%m-%d-%Y",
                "%Y年%m月%d日", "%d.%m.%Y", "%m.%d.%Y"
            ]

            for fmt in formats:
                try:
                    dt = datetime.strptime(date_str, fmt)
                    return dt.strftime("%Y-%m-%d")
                except ValueError:
                    continue

            # dateutil使わない簡易パース
            # 数字を抽出して年月日として解釈
            numbers = re.findall(r'\d+', date_str)
            if len(numbers) >= 3:
                year = int(numbers[0])
                month = int(numbers[1])
                day = int(numbers[2])

                # 年が2桁の場合の処理
                if year < 100:
                    year += 2000 if year < 50 else 1900

                # 日月年の可能性もチェック
                if day > 31 and year < 31:
                    year, day = day, year

                if 1 <= month <= 12 and 1 <= day <= 31:
                    try:
                        dt = datetime(year, month, day)
                        return dt.strftime("%Y-%m-%d")
                    except ValueError:
                        pass

            return ""
        except:
            return ""

    @staticmethod
    def TIMEVALUE(time_string: Any) -> str:
        """
        時刻文字列を標準時刻形式に変換

        Args:
            time_string: 時刻を表す文字列

        Returns:
            標準形式の時刻文字列（HH:MM:SS）
        """
        try:
            time_str = str(time_string)
            # 様々な形式を試す
            formats = [
                "%H:%M:%S", "%H:%M", "%I:%M:%S %p", "%I:%M %p",
                "%H時%M分%S秒", "%H時%M分", "%H.%M.%S", "%H.%M"
            ]

            for fmt in formats:
                try:
                    dt = datetime.strptime(time_str, fmt)
                    return dt.strftime("%H:%M:%S")
                except ValueError:
                    continue

            # 数字のみの場合（HHMMSS形式など）
            numbers = re.findall(r'\d+', time_str)
            if len(numbers) >= 2:
                hour = int(numbers[0])
                minute = int(numbers[1])
                second = int(numbers[2]) if len(numbers) >= 3 else 0

                # 時刻の妥当性チェック
                if 0 <= hour < 24 and 0 <= minute < 60 and 0 <= second < 60:
                    return f"{hour:02d}:{minute:02d}:{second:02d}"

            return ""
        except:
            return ""

    @staticmethod
    def TIMER() -> float:
        """
        午前0時からの秒数を返す

        Returns:
            午前0時からの経過秒数
        """
        try:
            now = datetime.now()
            midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
            delta = now - midnight
            return delta.total_seconds()
        except:
            return 0.0

    @staticmethod
    def CDATE(date_string: Any) -> str:
        """
        日付文字列を日付型に変換（VBA互換）

        柔軟なフォーマット対応：
        - 完全な日時: "2025/11/05 15:39:49" → 2025/11/05 15:39:49
        - 日付のみ: "2025/11/05" → 2025/11/05 00:00:00
        - 年月のみ: "2025/11" → 2025/11/1 00:00:00
        - 年のみ: "2025" → 2025/1/1 00:00:00
        - 時刻の部分補完: "2025/11/05 15" → 2025/11/05 15:00:00
        - 時刻の部分補完: "2025/11/05 15:39" → 2025/11/05 15:39:00

        区切り文字の柔軟性：
        - "/" と "-" の混在を許容
        - "2025-11-05-15-39-49" も許容
        - "2025-11-05 15-39-49" も許容
        - "2025-11-05 15:39:49" も許容

        Args:
            date_string: 日付を表す文字列

        Returns:
            日付文字列（YYYY/MM/DD HH:MM:SS形式）
        """
        try:
            date_str = str(date_string).strip()

            # 区切り文字を正規化（"/" と "-" と ":" と空白を統一区切りとして扱う）
            # 数字のみを抽出
            numbers = re.findall(r'\d+', date_str)

            if not numbers:
                return ""

            # デフォルト値
            year = 1
            month = 1
            day = 1
            hour = 0
            minute = 0
            second = 0

            # 数字の個数に応じて解析
            if len(numbers) >= 1:
                year = int(numbers[0])
            if len(numbers) >= 2:
                month = int(numbers[1])
            if len(numbers) >= 3:
                day = int(numbers[2])
            if len(numbers) >= 4:
                hour = int(numbers[3])
            if len(numbers) >= 5:
                minute = int(numbers[4])
            if len(numbers) >= 6:
                second = int(numbers[5])

            # 年が2桁の場合の処理（2000年代として扱う）
            if year < 100:
                year += 2000 if year < 50 else 1900

            # datetime型を生成
            dt = datetime(year, month, day, hour, minute, second)

            # YYYY/MM/DD HH:MM:SS形式で返す
            return dt.strftime("%Y/%m/%d %H:%M:%S")

        except Exception as e:
            # エラー時は空文字列を返す
            return ""