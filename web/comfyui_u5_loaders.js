/**
 * ComfyUI U5 Loaders UI Extension
 * u5ローダーシリーズのUI制御（text_input連動時のセレクトボックス更新）
 */

// ファイル読み込み確認ログ
console.log('[u5_loaders] FILE LOADED - u5_loaders.js is being executed');

import { app } from "../../../scripts/app.js";

console.log('[u5_loaders] Import successful, app object:', app);

// ローダーごとの設定
const LOADER_CONFIGS = {
    'u5_CheckpointLoader': {
        widgetName: 'ckpt_name',
        filenameOutputIndex: 3  // 4番目の出力（0-indexed）
    },
    'u5_LoraLoader': {
        widgetName: 'lora_name',
        filenameOutputIndex: 2  // 3番目の出力
    },
    'u5_VAELoader': {
        widgetName: 'vae_name',
        filenameOutputIndex: 1  // 2番目の出力
    },
    'u5_ControlNetLoader': {
        widgetName: 'control_net_name',
        filenameOutputIndex: 1  // 2番目の出力
    },
    'u5_CLIPVisionLoader': {
        widgetName: 'clip_name',
        filenameOutputIndex: 1  // 2番目の出力
    },
    'u5_StyleModelLoader': {
        widgetName: 'style_model_name',
        filenameOutputIndex: 1  // 2番目の出力
    },
    'u5_GLIGENLoader': {
        widgetName: 'gligen_name',
        filenameOutputIndex: 1  // 2番目の出力
    },
    'u5_UNETLoader': {
        widgetName: 'unet_name',
        filenameOutputIndex: 1  // 2番目の出力
    },
    'u5_CLIPLoader': {
        widgetName: 'clip_name',
        filenameOutputIndex: 1  // 2番目の出力
    }
};

/**
 * デバッグログ出力
 * @param {...any} args - ログ出力する引数
 */
function debugLog(...args) {
    console.log('[u5_loaders]', ...args);
}

/**
 * セレクトボックスwidgetの値を更新
 * @param {Object} node - ComfyUIノード
 * @param {string} widgetName - 更新対象のwidget名
 * @param {string} newValue - 新しい値
 */
function updateSelectWidget(node, widgetName, newValue) {
    debugLog(`updateSelectWidget called:`, {
        nodeId: node?.id,
        widgetName,
        newValue,
        hasNode: !!node,
        hasWidgets: !!node?.widgets,
        widgetCount: node?.widgets?.length
    });

    if (!node || !widgetName || !newValue) {
        debugLog('Invalid parameters - aborting update');
        return;
    }

    // 全widgetをリスト表示
    debugLog(`Available widgets in node ${node.id}:`,
        node.widgets?.map(w => ({ name: w.name, type: w.type, value: w.value }))
    );

    // widgetを検索
    const widget = node.widgets?.find(w => w.name === widgetName);
    if (!widget) {
        debugLog(`ERROR: Widget "${widgetName}" not found in node ${node.id}`);
        return;
    }

    // 値を更新
    const oldValue = widget.value;
    debugLog(`Found widget "${widgetName}", updating value:`, {
        oldValue,
        newValue,
        widgetType: widget.type
    });

    widget.value = newValue;

    debugLog(`Widget value updated successfully`);

    // UIを再描画
    if (node.setDirtyCanvas) {
        node.setDirtyCanvas(true, true);
        debugLog(`Canvas marked as dirty for redraw`);
    }

    // widgetのcallbackを呼び出す（存在する場合）
    if (widget.callback) {
        debugLog(`Calling widget callback`);
        widget.callback(newValue);
    } else {
        debugLog(`No callback found for widget`);
    }

    debugLog(`updateSelectWidget complete`);
}

/**
 * ノードにonExecutedフックを追加
 * @param {Object} node - ComfyUIノードインスタンス
 * @param {Object} config - ローダー設定
 */
function addOnExecutedHook(node, config) {
    const originalOnExecuted = node.onExecuted;

    node.onExecuted = function(message) {
        console.log('[u5_loaders] onExecuted called for:', node.type, 'node', node.id);
        console.log('[u5_loaders] Message structure:', JSON.stringify(message, null, 2));
        console.log('[u5_loaders] Config:', config);

        // 元のonExecutedハンドラを呼び出し
        const r = originalOnExecuted ? originalOnExecuted.apply(this, arguments) : undefined;

        // メッセージ構造を確認するための詳細ログ
        console.log('[u5_loaders] Message keys:', Object.keys(message || {}));
        console.log('[u5_loaders] Message type:', typeof message);
        console.log('[u5_loaders] Is Array:', Array.isArray(message));

        // 複数のアクセス方法を試す
        let selectedFilename = null;

        // 方法1: 数値インデックス直接アクセス
        selectedFilename = message?.[config.filenameOutputIndex];
        console.log('[u5_loaders] Method 1 (direct index', config.filenameOutputIndex + '):', selectedFilename);

        // 方法2: 文字列キーとしてアクセス
        if (!selectedFilename) {
            selectedFilename = message?.[String(config.filenameOutputIndex)];
            console.log('[u5_loaders] Method 2 (string key "' + config.filenameOutputIndex + '"):', selectedFilename);
        }

        // 方法3: RETURN_NAMESの"filename"キーでアクセス
        if (!selectedFilename) {
            selectedFilename = message?.['filename'];
            console.log('[u5_loaders] Method 3 (key "filename"):', selectedFilename);
        }

        // 方法4: 配列の場合
        if (!selectedFilename && Array.isArray(message)) {
            selectedFilename = message[config.filenameOutputIndex];
            console.log('[u5_loaders] Method 4 (array access):', selectedFilename);
        }

        if (!selectedFilename) {
            console.log('[u5_loaders] No filename found for', node.type, 'node', node.id);
            console.log('[u5_loaders] Tried all methods for output index', config.filenameOutputIndex);
            return r;
        }

        console.log('[u5_loaders] Selected filename:', selectedFilename);

        // セレクトボックスを更新
        updateSelectWidget(node, config.widgetName, selectedFilename);

        return r;
    };

    console.log('[u5_loaders] onExecuted hook added to node', node.id, 'type:', node.type);
}

// app拡張を登録
console.log('[u5_loaders] Registering extension "u5.loaders"');

app.registerExtension({
    name: "u5.loaders",

    async setup() {
        // カスタムイベントリスナーを登録（Python側からのUI更新メッセージ）
        app.api.addEventListener("u5_widget_update", (event) => {
            debugLog('Received u5_widget_update event:', event.detail);

            const { node_type, widget_name, new_value, unique_id } = event.detail;

            if (!node_type || !widget_name || !new_value) {
                debugLog('Invalid event data, ignoring');
                return;
            }

            // 該当するノードを検索
            let targetNodes = [];
            if (unique_id) {
                // unique_idが指定されている場合は特定のノードのみ更新
                const node = app.graph._nodes_by_id?.[unique_id];
                if (node) targetNodes.push(node);
            } else {
                // unique_idがない場合は、該当タイプの全ノードを更新
                targetNodes = app.graph._nodes.filter(n => n.type === node_type);
            }

            debugLog(`Found ${targetNodes.length} target node(s) for type "${node_type}"`);

            // 各ノードのwidgetを更新
            targetNodes.forEach(node => {
                debugLog(`Updating node ${node.id} (${node.type})`);
                updateSelectWidget(node, widget_name, new_value);
            });
        });

        debugLog('Custom event listener "u5_widget_update" registered');
    },

    async nodeCreated(node) {
        // ノード作成時にu5ローダーシリーズかチェック
        const config = LOADER_CONFIGS[node.type];
        if (!config) {
            return;  // 対象外のノードはスキップ
        }

        console.log('[u5_loaders] u5 loader node created:', node.type, 'node', node.id);

        // onExecutedフックを追加（後方互換性のため残す）
        addOnExecutedHook(node, config);
    }
});
