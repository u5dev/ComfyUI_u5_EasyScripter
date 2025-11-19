# -*- coding: utf-8 -*-
"""
http_functions.py

HTTP/HTTPS通信機能を提供するビルトイン関数群
外部RestAPIとの通信をcurl風に実行可能
"""

import urllib.request
import urllib.parse
import urllib.error
import json as json_module
from typing import Optional, Dict, Any


class HttpFunctions:
    """HTTP/HTTPS通信機能クラス"""

    # 最後のHTTPレスポンス情報を保持（クラス変数）
    _last_status_code: int = 0
    _last_headers: Dict[str, str] = {}

    @staticmethod
    def HTTPGET(url: str, headers: Optional[str] = None) -> str:
        """
        HTTP GETリクエストを送信

        Args:
            url: リクエストURL
            headers: HTTPヘッダー（オプション、改行区切り "Key: Value" 形式）

        Returns:
            レスポンスボディ（文字列）
        """
        return HttpFunctions._http_request("GET", url, headers=headers)

    @staticmethod
    def HTTPPOST(url: str, body: str, headers: Optional[str] = None) -> str:
        """
        HTTP POSTリクエストを送信

        Args:
            url: リクエストURL
            body: リクエストボディ
            headers: HTTPヘッダー（オプション、改行区切り "Key: Value" 形式）

        Returns:
            レスポンスボディ（文字列）
        """
        return HttpFunctions._http_request("POST", url, body=body, headers=headers)

    @staticmethod
    def HTTPPUT(url: str, body: str, headers: Optional[str] = None) -> str:
        """
        HTTP PUTリクエストを送信

        Args:
            url: リクエストURL
            body: リクエストボディ
            headers: HTTPヘッダー（オプション、改行区切り "Key: Value" 形式）

        Returns:
            レスポンスボディ（文字列）
        """
        return HttpFunctions._http_request("PUT", url, body=body, headers=headers)

    @staticmethod
    def HTTPDELETE(url: str, headers: Optional[str] = None) -> str:
        """
        HTTP DELETEリクエストを送信

        Args:
            url: リクエストURL
            headers: HTTPヘッダー（オプション、改行区切り "Key: Value" 形式）

        Returns:
            レスポンスボディ（文字列）
        """
        return HttpFunctions._http_request("DELETE", url, headers=headers)

    @staticmethod
    def HTTPJSON(url: str, method: str, json_body: Optional[str] = None, headers: Optional[str] = None) -> str:
        """
        JSON形式でHTTP通信を実行（Content-Type: application/json自動設定）

        Args:
            url: リクエストURL
            method: HTTPメソッド（GET/POST/PUT/DELETE）
            json_body: JSONリクエストボディ（オプション、文字列形式）
            headers: 追加HTTPヘッダー（オプション）

        Returns:
            パースされたJSONレスポンス（JSON文字列として返却）
        """
        # Content-Type: application/jsonを自動追加
        json_header = "Content-Type: application/json"
        if headers:
            combined_headers = f"{headers}\n{json_header}"
        else:
            combined_headers = json_header

        response = HttpFunctions._http_request(
            method.upper(),
            url,
            body=json_body,
            headers=combined_headers
        )

        # JSONレスポンスをパースして返却
        try:
            parsed_json = json_module.loads(response)
            # 辞書を再度JSON文字列化して返す（EasyScripter互換性）
            return json_module.dumps(parsed_json, ensure_ascii=False)
        except json_module.JSONDecodeError:
            # JSONパース失敗時はそのまま返却
            return response

    @staticmethod
    def HTTPSTATUS() -> int:
        """
        最後のHTTPリクエストのステータスコードを取得

        Returns:
            ステータスコード（整数）
        """
        return HttpFunctions._last_status_code

    @staticmethod
    def HTTPHEADERS() -> str:
        """
        最後のHTTPレスポンスヘッダーを取得

        Returns:
            ヘッダー辞書（JSON文字列）
        """
        return json_module.dumps(HttpFunctions._last_headers, ensure_ascii=False)

    @staticmethod
    def _http_request(
        method: str,
        url: str,
        body: Optional[str] = None,
        headers: Optional[str] = None
    ) -> str:
        """
        HTTP/HTTPSリクエストを送信する内部メソッド

        Args:
            method: HTTPメソッド(GET/POST/PUT/DELETE)
            url: リクエストURL（URLエンコードはユーザーが行う）
            body: リクエストボディ(オプション)
            headers: HTTPヘッダー(オプション、改行区切り "Key: Value" 形式)

        Returns:
            レスポンスボディ(文字列)
        """
        # リクエストボディをバイト列に変換
        data = body.encode('utf-8') if body else None

        # HTTPヘッダーをパース
        header_dict = HttpFunctions._parse_headers(headers) if headers else {}

        # HTTPリクエストを作成
        req = urllib.request.Request(
            url,
            data=data,
            headers=header_dict,
            method=method
        )

        try:
            # リクエスト送信
            with urllib.request.urlopen(req) as response:
                # ステータスコードとヘッダーを保存
                HttpFunctions._last_status_code = response.status
                HttpFunctions._last_headers = dict(response.headers)

                # レスポンスボディを読み込み
                response_body = response.read().decode('utf-8')
                return response_body

        except urllib.error.HTTPError as e:
            # HTTPエラー(4xx, 5xx)
            HttpFunctions._last_status_code = e.code
            HttpFunctions._last_headers = dict(e.headers)

            # エラーレスポンスボディを読み込み
            error_body = e.read().decode('utf-8') if e.fp else ""
            return error_body

        except urllib.error.URLError as e:
            # URL/ネットワークエラー
            HttpFunctions._last_status_code = 0
            HttpFunctions._last_headers = {}
            raise RuntimeError(f"HTTP通信エラー: {str(e)}")

        except Exception as e:
            # その他のエラー
            HttpFunctions._last_status_code = 0
            HttpFunctions._last_headers = {}
            raise RuntimeError(f"予期しないHTTPエラー: {str(e)}")

    @staticmethod
    def _parse_headers(headers: str) -> Dict[str, str]:
        """
        ヘッダー文字列をパースして辞書に変換

        Args:
            headers: ヘッダー文字列（改行区切り "Key: Value" 形式）

        Returns:
            ヘッダー辞書
        """
        header_dict = {}

        for line in headers.split('\n'):
            line = line.strip()
            if ':' in line:
                key, value = line.split(':', 1)
                header_dict[key.strip()] = value.strip()

        return header_dict


class JsonFunctions:
    """JSON操作機能クラス"""

    @staticmethod
    def PARSEJSON(json_string: str) -> Any:
        """
        JSON文字列をパースしてPythonオブジェクト（辞書/リスト）に変換

        Args:
            json_string: JSON形式の文字列

        Returns:
            パースされたPythonオブジェクト（辞書、リスト、プリミティブ値）

        Example:
            json_obj = PARSEJSON('{"name": "John", "age": 30}')
            # json_obj = {"name": "John", "age": 30}
        """
        if not isinstance(json_string, str):
            raise TypeError(f"PARSEJSON: 引数は文字列である必要があります（受け取った型: {type(json_string).__name__}）")

        try:
            return json_module.loads(json_string)
        except json_module.JSONDecodeError as e:
            raise RuntimeError(f"JSON解析エラー: {str(e)}")

    @staticmethod
    def GETJSON(json_obj: Any, key_path: str) -> Any:
        """
        JSONオブジェクトから指定されたキーパスで値を取得

        Args:
            json_obj: JSONオブジェクト（辞書またはリスト）
            key_path: キーパス（ドット記法: "result.description" または単一キー: "name"）

        Returns:
            取得された値（文字列、数値、辞書、リスト等）

        Example:
            json_obj = PARSEJSON('{"result": {"description": "test"}}')
            description = GETJSON(json_obj, "result.description")
            # description = "test"

            json_obj = PARSEJSON('{"items": [1, 2, 3]}')
            item = GETJSON(json_obj, "items.0")
            # item = 1
        """
        if not isinstance(key_path, str):
            raise TypeError(f"GETJSON: key_pathは文字列である必要があります（受け取った型: {type(key_path).__name__}）")

        # キーパスを分割（ドット記法対応）
        keys = key_path.split('.')

        # 現在のオブジェクトから順にキーをたどる
        current_obj = json_obj

        for key in keys:
            if isinstance(current_obj, dict):
                # 辞書の場合、キーで取得
                if key not in current_obj:
                    raise RuntimeError(f"JSONキーエラー: キー '{key}' が見つかりません（パス: {key_path}）")
                current_obj = current_obj[key]

            elif isinstance(current_obj, list):
                # リストの場合、インデックスで取得
                try:
                    index = int(key)
                    if index < 0 or index >= len(current_obj):
                        raise RuntimeError(f"JSONインデックスエラー: インデックス {index} が範囲外です（リスト長: {len(current_obj)}）")
                    current_obj = current_obj[index]
                except ValueError:
                    raise RuntimeError(f"JSONインデックスエラー: リストに対してインデックス '{key}' が無効です（整数が必要）")

            else:
                # プリミティブ値の場合、これ以上たどれない
                raise RuntimeError(f"JSONパスエラー: '{key}' にアクセスできません（現在の値の型: {type(current_obj).__name__}）")

        return current_obj

    @staticmethod
    def TOJSON(value: Any) -> str:
        """
        PythonオブジェクトをJSON文字列に変換

        Args:
            value: JSON化する値（辞書、リスト、文字列、数値等）

        Returns:
            JSON文字列

        Example:
            json_str = TOJSON({"name": "John", "age": 30})
            # json_str = '{"name": "John", "age": 30}'
        """
        try:
            return json_module.dumps(value, ensure_ascii=False)
        except (TypeError, ValueError) as e:
            raise RuntimeError(f"JSON変換エラー: {str(e)}")
