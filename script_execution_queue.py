# -*- coding: utf-8 -*-
"""
ScriptExecutionQueue - EasyScripter並行実行制御機構

目的:
- ComfyUI実行中にEasyScripterノードが並行起動された際のハングアップを防止
- FIFOキューによる順次実行制御
- エラー発生時もキューを継続

アーキテクチャ:
- シングルトンパターン: 全EasyScripterノードで1つのキューを共有
- ワーカースレッド: バックグラウンドでキューからタスクを取り出して実行
- スレッドセーフ: threading.Queueとthreading.Lockで排他制御

使用方法:
    queue = ScriptExecutionQueue.get_instance()
    result = queue.enqueue_and_wait(task_callable, *args, **kwargs)
"""

import queue
import threading
import time
import traceback
from typing import Callable, Any, Dict, Optional

# CRITICAL: グローバルインポート（関数内動的インポート禁止ルールに準拠）
# ComfyUI環境では関数内動的インポートがModuleNotFoundErrorを引き起こす
try:
    from .locales import get_message
except ImportError:
    from locales import get_message


class ScriptExecutionQueue:
    """EasyScripterスクリプト実行の順次制御キュー（シングルトン）"""

    _instance: Optional['ScriptExecutionQueue'] = None
    _lock = threading.Lock()

    @classmethod
    def get_instance(cls, locale: str = 'ja') -> 'ScriptExecutionQueue':
        """シングルトンインスタンスを取得"""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:  # ダブルチェックロッキング
                    cls._instance = cls(locale=locale)
        return cls._instance

    def __init__(self, locale: str = 'ja'):
        """初期化（外部から直接呼び出し禁止、get_instance()を使用）"""
        if ScriptExecutionQueue._instance is not None:
            raise RuntimeError(get_message('queue_error_singleton', locale))

        self.locale = locale
        self._get_message = get_message

        self._queue: queue.Queue = queue.Queue()
        self._worker_thread: Optional[threading.Thread] = None
        self._running = False
        self._current_task_id: Optional[str] = None
        self._current_task_lock = threading.Lock()

        # ワーカースレッド起動
        self._start_worker()

        print(self._get_message('queue_initialized', self.locale))

    def _start_worker(self):
        """ワーカースレッドを起動"""
        if self._worker_thread is not None and self._worker_thread.is_alive():
            return  # 既に起動済み

        self._running = True
        self._worker_thread = threading.Thread(target=self._worker_loop, daemon=True)
        self._worker_thread.start()

    def _worker_loop(self):
        """ワーカースレッドのメインループ"""
        print(self._get_message('queue_worker_started', self.locale))

        while self._running:
            try:
                # キューからタスクを取得（タイムアウト1秒）
                task_item = self._queue.get(timeout=1.0)

                task_id = task_item["task_id"]
                task_callable = task_item["callable"]
                args = task_item["args"]
                kwargs = task_item["kwargs"]
                result_container = task_item["result_container"]

                # 現在実行中のタスクIDを記録
                with self._current_task_lock:
                    self._current_task_id = task_id

                print(self._get_message('queue_task_started', self.locale, task_id))

                try:
                    # タスク実行
                    start_time = time.time()
                    result = task_callable(*args, **kwargs)
                    elapsed = time.time() - start_time

                    # 結果を格納
                    result_container["result"] = result
                    result_container["error"] = None
                    result_container["completed"] = True

                    print(self._get_message('queue_task_completed', self.locale, task_id, elapsed))

                except Exception as e:
                    # エラー発生時
                    error_msg = f"{type(e).__name__}: {str(e)}"
                    print(self._get_message('queue_task_error', self.locale, task_id, error_msg))
                    traceback.print_exc()

                    # エラー情報を格納
                    result_container["result"] = None
                    result_container["error"] = e
                    result_container["completed"] = True

                finally:
                    # 現在実行中のタスクIDをクリア
                    with self._current_task_lock:
                        self._current_task_id = None

                    # キューのタスク完了を通知
                    self._queue.task_done()

            except queue.Empty:
                # タイムアウト（キューが空）
                continue

            except Exception as e:
                # ワーカースレッド自体のエラー（回復不能）
                print(self._get_message('queue_worker_fatal_error', self.locale, e))
                traceback.print_exc()
                break

        print(self._get_message('queue_worker_stopped', self.locale))

    def enqueue_and_wait(
        self,
        task_callable: Callable[..., Any],
        task_id: Optional[str] = None,
        timeout: Optional[float] = None,
        *args,
        **kwargs
    ) -> Any:
        """タスクをキューに追加し、完了まで待機

        Args:
            task_callable: 実行する関数
            task_id: タスクID（デバッグ用、Noneの場合は自動生成）
            timeout: タイムアウト秒数（Noneの場合は無制限）
            *args: task_callableの位置引数
            **kwargs: task_callableのキーワード引数

        Returns:
            Any: task_callableの戻り値

        Raises:
            Exception: task_callable内で発生した例外
            TimeoutError: タイムアウト発生時
        """
        if task_id is None:
            task_id = f"task_{threading.get_ident()}_{time.time()}"

        # ========================================
        # DIAG-2: ワーカースレッド生存確認
        # ========================================
        worker_alive = self._worker_thread.is_alive() if self._worker_thread else False
        queue_size_before = self._queue.qsize()
        
        print(self._get_message('queue_diag2_enqueue_call', self.locale, 
                                task_id, worker_alive, queue_size_before, self._running))
        
        if not worker_alive:
            print(self._get_message('queue_diag2_worker_stopped', self.locale,
                                    self._running, self._worker_thread))

        # 結果格納用コンテナ（スレッド間共有）
        result_container: Dict[str, Any] = {
            "result": None,
            "error": None,
            "completed": False
        }

        # タスクアイテム作成
        task_item = {
            "task_id": task_id,
            "callable": task_callable,
            "args": args,
            "kwargs": kwargs,
            "result_container": result_container
        }

        # キューに追加
        self._queue.put(task_item)
        queue_size = self._queue.qsize()
        print(self._get_message('queue_task_enqueued', self.locale, task_id, queue_size))

        # 完了まで待機（ポーリング方式）
        start_wait_time = time.time()
        poll_count = 0
        while not result_container["completed"]:
            poll_count += 1
            time.sleep(0.05)  # 50ms間隔でチェック

            # ========================================
            # DIAG-3: タスク実行フロー詳細追跡（1秒ごと）
            # ========================================
            if poll_count % 20 == 0:  # 20 * 0.05s = 1秒
                elapsed = time.time() - start_wait_time
                current_task = self.get_current_task_id()
                print(self._get_message('queue_diag3_waiting', self.locale,
                                        task_id, elapsed, result_container['completed'],
                                        current_task, self._queue.qsize()))

            # タイムアウトチェック
            if timeout is not None:
                elapsed = time.time() - start_wait_time
                if elapsed > timeout:
                    # タイムアウト時の詳細ログ
                    worker_alive_check = self._worker_thread.is_alive() if self._worker_thread else False
                    print(self._get_message('queue_diag3_timeout', self.locale,
                                            task_id, elapsed, worker_alive_check,
                                            self._queue.qsize(), self.get_current_task_id()))
                    raise TimeoutError(
                        self._get_message('queue_task_timeout', self.locale, task_id, timeout)
                    )

        # 結果を返却
        if result_container["error"] is not None:
            # エラーが発生していた場合、再スロー
            raise result_container["error"]

        return result_container["result"]

    def get_current_task_id(self) -> Optional[str]:
        """現在実行中のタスクIDを取得"""
        with self._current_task_lock:
            return self._current_task_id

    def get_queue_size(self) -> int:
        """キューの待機タスク数を取得"""
        return self._queue.qsize()

    def is_executing(self) -> bool:
        """現在タスク実行中かどうか"""
        with self._current_task_lock:
            return self._current_task_id is not None

    def shutdown(self):
        """ワーカースレッドを停止（テスト用）"""
        print(self._get_message('queue_shutdown_request', self.locale))
        self._running = False

        if self._worker_thread is not None:
            self._worker_thread.join(timeout=5.0)

        print(self._get_message('queue_shutdown_complete', self.locale))


# モジュールレベルでの便利関数
def get_execution_queue(locale: str = 'ja') -> ScriptExecutionQueue:
    """グローバルなScriptExecutionQueueインスタンスを取得"""
    return ScriptExecutionQueue.get_instance(locale=locale)
