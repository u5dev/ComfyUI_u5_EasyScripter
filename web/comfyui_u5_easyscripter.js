/**
 * ComfyUI U5 EasyScripter Web UI Component
 * スクリプト入力と標準出力表示のためのUI拡張
 * 多言語対応版
 */

import { app } from "../../../scripts/app.js";
import { api } from "../../../scripts/api.js";
import { ComfyWidgets } from "../../../scripts/widgets.js";

// 言語検出関数
function getUserLocale() {
    const lang = navigator.language || navigator.userLanguage || 'en';
    return lang.toLowerCase().startsWith('ja') ? 'ja' : 'en';
}

// メッセージの翻訳マップ
const MESSAGES = {
    'en': {
        '[Warning] No script provided': '[Warning] No script provided',
        '[警告] スクリプトが提供されていません': '[Warning] No script provided',
        '[Warning] RETURN was not assigned; defaulting to 0': '[Warning] RETURN was not assigned; defaulting to 0',
        '[警告] RETURNが代入されていません。デフォルトの0を使用します': '[Warning] RETURN was not assigned; defaulting to 0',
        '[Error]': '[Error]',
        '[エラー]': '[Error]',
        'Script output will appear here...': 'Script output will appear here...',
    },
    'ja': {
        '[Warning] No script provided': '[警告] スクリプトが提供されていません',
        '[警告] スクリプトが提供されていません': '[警告] スクリプトが提供されていません',
        '[Warning] RETURN was not assigned; defaulting to 0': '[警告] RETURNが代入されていません。デフォルトの0を使用します',
        '[警告] RETURNが代入されていません。デフォルトの0を使用します': '[警告] RETURNが代入されていません。デフォルトの0を使用します',
        '[Error]': '[エラー]',
        '[エラー]': '[エラー]',
        'Script output will appear here...': 'スクリプトの出力がここに表示されます...',
    }
};

// メッセージを翻訳する関数
function translateMessage(text, locale) {
    if (!text) return text;

    const messages = MESSAGES[locale] || MESSAGES['en'];

    // 各メッセージパターンを置換
    let translatedText = text;
    for (const [pattern, replacement] of Object.entries(messages)) {
        translatedText = translatedText.replace(new RegExp(pattern.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'g'), replacement);
    }

    return translatedText;
}

/**
 * デバッグログ出力（UI_CONFIG.debug.enabledで制御）
 * @param {...any} args - ログ出力する引数
 */
function debugLog(...args) {
    if (UI_CONFIG.debug.enabled) {
        console.log('[comfyUI_u5_easyscripter]', ...args);
    }
}

/**
 * 入力ソケットエリアの実際の高さを計算
 * @param {Object} node - ComfyUIノードオブジェクト
 * @returns {number} 入力ソケットエリアの高さ（ピクセル）
 */
function calculateInputSocketAreaHeight(node) {
    // 入力ソケット数を取得（optional入力のみカウント）
    const inputCount = node.inputs ? node.inputs.length : 0;

    if (inputCount === 0) {
        // 入力ソケットがない場合は最小値を返す
        return UI_CONFIG.layout.inputSocketAreaMin;
    }

    // 実際の高さを計算
    const calculatedHeight = UI_CONFIG.layout.nodeHeaderHeight +
                            (inputCount * (UI_CONFIG.layout.socketHeight + UI_CONFIG.layout.socketSpacing));

    // 最小値・最大値の範囲内に収める
    return Math.min(
        UI_CONFIG.layout.inputSocketAreaMax,
        Math.max(UI_CONFIG.layout.inputSocketAreaMin, calculatedHeight)
    );
}

/**
 * ウィジェット要素に共通スタイルを適用
 * @param {HTMLElement} element - スタイルを適用する要素
 * @param {Object} config - スタイル設定オブジェクト
 * @param {number} config.minHeight - 最小高さ
 * @param {number} config.maxHeight - 最大高さ
 * @param {string} config.backgroundColor - 背景色
 * @param {string} config.color - 文字色
 * @param {boolean} config.readOnly - 読み取り専用フラグ（オプション）
 * @param {boolean} config.isOutput - 出力ウィジェットかどうか（フォントサイズ/行間の調整用）
 */
function applyWidgetStyles(element, config) {
    if (!element) return;

    // フォントサイズと行間の決定（出力エリアとスクリプトエリアで異なる）
    const fontSize = config.isOutput ? UI_CONFIG.styling.outputFontSize : UI_CONFIG.styling.fontSize;
    const lineHeight = config.isOutput ? UI_CONFIG.styling.outputLineHeight : UI_CONFIG.styling.lineHeight;

    // 共通スタイル（可読性向上）
    element.style.fontFamily = "'Consolas', 'Monaco', 'Courier New', monospace";
    element.style.fontSize = `${fontSize}px`;
    element.style.border = "1px solid #3c3c3c";
    element.style.padding = `${UI_CONFIG.styling.padding}px`;
    element.style.lineHeight = `${lineHeight}`;
    element.style.overflow = "auto";
    element.style.width = `calc(100% - ${UI_CONFIG.styling.widthAdjustment}px)`;
    element.style.boxSizing = "border-box";
    element.style.marginLeft = `${UI_CONFIG.styling.margin}px`;

    // 個別設定
    if (config.minHeight !== undefined) {
        element.style.minHeight = `${config.minHeight}px`;
    }
    if (config.maxHeight !== undefined) {
        element.style.maxHeight = `${config.maxHeight}px`;
    }
    if (config.backgroundColor) {
        element.style.backgroundColor = config.backgroundColor;
    }
    if (config.color) {
        element.style.color = config.color;
    }
    if (config.readOnly) {
        element.readOnly = true;
        element.style.cursor = "default";
    }
    if (config.resize !== undefined) {
        element.style.resize = config.resize;
    }
}

/**
 * 実行結果メッセージを解析して表示用テキストに変換
 * @param {*} message - 実行結果メッセージ（様々な形式に対応）
 * @returns {string} 表示用テキスト
 */
function parseExecutionMessage(message) {
    if (!message) return "";

    let outputText = "";

    // メッセージから表示テキストを取得
    if (message.text !== undefined) {
        // text プロパティを処理
        if (Array.isArray(message.text)) {
            // 配列の場合、結合
            outputText = message.text.join('\n');
        } else if (typeof message.text === 'string') {
            // 文字列の場合、そのまま使用
            outputText = message.text;
        } else {
            outputText = String(message.text);
        }
    } else if (message.string !== undefined) {
        // 古い形式（stringプロパティ）
        outputText = String(message.string);
    } else if (Array.isArray(message)) {
        // 配列が直接渡された場合
        outputText = message.join('\n');
    } else if (typeof message === 'string') {
        // 文字列が直接渡された場合
        outputText = message;
    } else {
        // その他の場合、JSON形式で表示（デバッグ用）
        outputText = JSON.stringify(message, null, 2);
    }

    return outputText;
}

// ========================================
// ログ表示状態管理関数
// ========================================

/**
 * ログ表示状態を取得
 * @param {Object} node - ComfyUIノード
 * @returns {string} ログ表示状態（'collapsed'または'expanded'）
 */
function getLogDisplayState(node) {
    if (!node || !node.properties) return UI_CONFIG.logDisplay.defaultState;
    return node.properties[UI_CONFIG.logDisplay.stateProp] || UI_CONFIG.logDisplay.defaultState;
}

/**
 * ログ表示状態を設定
 * @param {Object} node - ComfyUIノード
 * @param {string} state - 設定する状態（'collapsed'または'expanded'）
 */
function setLogDisplayState(node, state) {
    if (!node || !node.properties) return;
    node.properties[UI_CONFIG.logDisplay.stateProp] = state;
    debugLog(`[LogToggle] State set to: ${state}`);
}

/**
 * ログエリアの折りたたみ機能を設定
 * @param {Object} node - ComfyUIノード
 * @param {Object} outputWidget - 出力ウィジェット
 */
function setupLogToggle(node, outputWidget) {
    debugLog('[LogToggle] setupLogToggle called', {
        hasOutputWidget: !!outputWidget,
        hasInputEl: !!outputWidget?.inputEl,
        inputElType: outputWidget?.inputEl?.tagName,
        inputElParent: outputWidget?.inputEl?.parentElement?.tagName
    });

    if (!outputWidget || !outputWidget.inputEl) {
        debugLog('[LogToggle] ABORT: outputWidget or inputEl not found');
        return;
    }

    // 初期状態の取得または設定
    let currentState = getLogDisplayState(node);
    if (!currentState) {
        currentState = UI_CONFIG.logDisplay.defaultState;
        setLogDisplayState(node, currentState);
    }
    debugLog('[LogToggle] Initial state:', currentState);

    // 既にwrapperが存在する場合はスキップ（重複初期化防止）
    const existingWrapper = outputWidget.inputEl.parentElement;
    if (existingWrapper && existingWrapper.classList.contains('easyscripter-output-wrapper')) {
        debugLog('[LogToggle] Wrapper already exists, skipping setup');
        return;
    }

    // ヘッダー要素を作成
    const header = document.createElement('div');
    header.className = 'easyscripter-output-header';
    header.style.cssText = `
        cursor: pointer;
        user-select: none;
        padding: 4px 8px;
        background-color: #2d2d30;
        border-bottom: 1px solid #3e3e42;
        display: flex;
        align-items: center;
        font-size: 12px;
        color: #cccccc;
    `;

    // インジケータアイコンを作成
    const icon = document.createElement('span');
    icon.className = 'easyscripter-toggle-icon';
    icon.textContent = currentState === LOG_DISPLAY_STATES.COLLAPSED ? '▶' : '▼';
    icon.style.cssText = `
        display: inline-block;
        margin-right: 6px;
        transition: transform 0.2s;
        font-size: 10px;
    `;

    // ラベルテキストを作成
    const label = document.createElement('span');
    label.textContent = 'Expand/Collapse Log';

    header.appendChild(icon);
    header.appendChild(label);

    // outputWidget.inputElの親要素にヘッダーを挿入
    const inputEl = outputWidget.inputEl;
    const parent = inputEl.parentElement;

    debugLog('[LogToggle] DOM structure:', {
        hasParent: !!parent,
        parentType: parent?.tagName,
        parentClassName: parent?.className,
        inputElNextSibling: !!inputEl.nextSibling
    });

    if (!parent) {
        debugLog('[LogToggle] ABORT: parent element not found');
        return;
    }

    // wrapper要素を作成
    const wrapper = document.createElement('div');
    wrapper.className = 'easyscripter-output-wrapper';
    wrapper.style.cssText = `
        position: relative;
        width: 100%;
    `;

    // inputElをwrapperで包む
    parent.insertBefore(wrapper, inputEl);
    wrapper.appendChild(header);
    wrapper.appendChild(inputEl);

    debugLog('[LogToggle] DOM structure created successfully');

    // クリックハンドラを設定
    const clickHandler = () => {
        const newState = currentState === LOG_DISPLAY_STATES.COLLAPSED
            ? LOG_DISPLAY_STATES.EXPANDED
            : LOG_DISPLAY_STATES.COLLAPSED;

        debugLog(`[LogToggle] Click detected! Toggling from ${currentState} to ${newState}`);

        // 状態を更新
        setLogDisplayState(node, newState);
        currentState = newState;

        // インジケータアイコンを更新
        icon.textContent = newState === LOG_DISPLAY_STATES.COLLAPSED ? '▶' : '▼';

        // レイアウトを更新
        updateLayoutForLogState(node);
    };

    header.addEventListener('click', clickHandler);
    debugLog('[LogToggle] Click handler attached');

    // ホバー時のスタイル
    header.addEventListener('mouseenter', () => {
        header.style.backgroundColor = '#3e3e42';
        debugLog('[LogToggle] Mouse enter');
    });
    header.addEventListener('mouseleave', () => {
        header.style.backgroundColor = '#2d2d30';
        debugLog('[LogToggle] Mouse leave');
    });

    // テスト用: ヘッダー要素にデータ属性を追加
    header.setAttribute('data-node-id', node.id);
    header.setAttribute('data-toggle-active', 'true');

    debugLog(`[LogToggle] Setup complete for node ${node.id}, initial state: ${currentState}`);
    debugLog('[LogToggle] Header element:', header);
    debugLog('[LogToggle] Click test - please click the "Output Log" header');
}

/**
 * ログ表示状態に応じてレイアウトを更新
 * @param {Object} node - ComfyUIノード
 */
function updateLayoutForLogState(node) {
    if (!node) return;

    const logState = getLogDisplayState(node);
    const outputWidget = node.widgets.find(w => w.name === 'output');
    const scriptWidget = node.widgets.find(w => w.name === 'script');

    if (!outputWidget || !outputWidget.inputEl) return;

    debugLog(`[LayoutUpdate] Updating layout for state: ${logState}`);

    // リサイズガードを有効化（MutationObserverの誤検知防止）
    node._easyscripter_resizing = true;

    // ユーザー手動リサイズフラグをリセット（折りたたみ操作は自動調整として扱う）
    node._user_manually_resized_script = false;

    // outputWidgetの高さを調整
    const outputHeight = logState === LOG_DISPLAY_STATES.COLLAPSED
        ? UI_CONFIG.widgets.output.collapsedHeight
        : UI_CONFIG.widgets.output.minHeight;

    // スタイル適用前のDOM実サイズを記録
    const beforeOutputHeight = outputWidget.inputEl.offsetHeight;
    const oldOutputWidgetHeight = outputWidget.height;
    debugLog(`[LayoutUpdate] OUTPUT BEFORE: offsetHeight=${beforeOutputHeight}px, widget.height=${oldOutputWidgetHeight}`);

    outputWidget.inputEl.style.height = `${outputHeight}px`;
    outputWidget.inputEl.style.minHeight = `${outputHeight}px`;

    // CRITICAL: computeSize関数を動的に変更してheightを制御（getter-only property回避）
    outputWidget.computeSize = function(width) {
        return [width, outputHeight];
    };
    debugLog(`[LayoutUpdate] OUTPUT computeSize updated to return height: ${outputHeight}`);

    // 折りたたみ時のスタイル調整
    if (logState === LOG_DISPLAY_STATES.COLLAPSED) {
        outputWidget.inputEl.style.overflow = 'hidden';
        outputWidget.inputEl.style.textOverflow = 'ellipsis';
        outputWidget.inputEl.style.whiteSpace = 'nowrap';
    } else {
        outputWidget.inputEl.style.overflow = 'auto';
        outputWidget.inputEl.style.textOverflow = 'clip';
        outputWidget.inputEl.style.whiteSpace = 'pre-wrap';
    }

    // スタイル適用直後のDOM実サイズを確認
    requestAnimationFrame(() => {
        const afterOutputHeight = outputWidget.inputEl.offsetHeight;
        const computedOutputStyle = window.getComputedStyle(outputWidget.inputEl);
        const newComputedHeight = outputWidget.computeSize(node.size[0])[1];
        debugLog(`[LayoutUpdate] OUTPUT AFTER: offsetHeight=${afterOutputHeight}px, computed.height=${computedOutputStyle.height}, computeSize()=${newComputedHeight}`);
        debugLog(`[LayoutUpdate] OUTPUT CHANGE: ${beforeOutputHeight}px → ${afterOutputHeight}px (${afterOutputHeight - beforeOutputHeight > 0 ? '+' : ''}${afterOutputHeight - beforeOutputHeight}px)`);
    });

    // scriptWidgetのサイズと位置を直接調整
    if (scriptWidget && scriptWidget.inputEl) {
        // CRITICAL: computeSizeHeightの固定値を使用（動的計算をやめる）
        const scriptHeight = UI_CONFIG.widgets.script.computeSizeHeight;

        debugLog(`[LayoutUpdate] Using fixed scriptHeight=${scriptHeight}px from computeSizeHeight`);

        // スタイル適用前のDOM実サイズを記録
        const beforeHeight = scriptWidget.inputEl.offsetHeight;
        const beforeClientHeight = scriptWidget.inputEl.clientHeight;
        const oldComputedHeight = scriptWidget.computeSize(node.size[0])[1];
        debugLog(`[LayoutUpdate] BEFORE: offsetHeight=${beforeHeight}px, clientHeight=${beforeClientHeight}px, computeSize()=${oldComputedHeight}`);

        // scriptWidgetの高さを更新（DOM要素）
        scriptWidget.inputEl.style.minHeight = `${scriptHeight}px`;
        scriptWidget.inputEl.style.maxHeight = `${scriptHeight + UI_CONFIG.widgets.script.maxHeightExtra}px`;
        scriptWidget.inputEl.style.height = `${scriptHeight}px`;

        // CRITICAL: computeSize関数を固定値に設定（動的計算しない）
        scriptWidget.computeSize = function(width) {
            return [width, UI_CONFIG.widgets.script.computeSizeHeight];
        };
        debugLog(`[LayoutUpdate] scriptWidget computeSize set to fixed height: ${UI_CONFIG.widgets.script.computeSizeHeight}`);

        // スタイル適用直後のDOM実サイズと計算済みスタイルを確認
        requestAnimationFrame(() => {
            const afterHeight = scriptWidget.inputEl.offsetHeight;
            const afterClientHeight = scriptWidget.inputEl.clientHeight;
            const computedStyle = window.getComputedStyle(scriptWidget.inputEl);
            const computedHeight = computedStyle.height;
            const computedMinHeight = computedStyle.minHeight;
            const computedMaxHeight = computedStyle.maxHeight;
            const newComputedHeight = scriptWidget.computeSize(node.size[0])[1];

            debugLog(`[LayoutUpdate] AFTER: offsetHeight=${afterHeight}px, clientHeight=${afterClientHeight}px, computeSize()=${newComputedHeight}`);
            debugLog(`[LayoutUpdate] COMPUTED: height=${computedHeight}, minHeight=${computedMinHeight}, maxHeight=${computedMaxHeight}`);
            debugLog(`[LayoutUpdate] CHANGE: offsetHeight ${beforeHeight}px → ${afterHeight}px (${afterHeight - beforeHeight > 0 ? '+' : ''}${afterHeight - beforeHeight}px)`);
        });

        // scriptWidgetのY座標を設定（ログエリアの下にスペースを空けて配置）
        // ComfyUIのデフォルト動作ではoutputWidgetが先に配置されるため、scriptWidgetのY座標のみ調整
        if (scriptWidget.inputEl) {
            // DOM要素のtop位置でスペースを追加（30px → 20px → 23pxに変更：3px下に移動）
            scriptWidget.inputEl.style.marginTop = '23px';
            debugLog(`[LayoutUpdate] Set scriptWidget marginTop to 23px`);
        }
    }

    // ノード全体の再レイアウトを強制（ComfyUIの連続描画に対抗）
    // CRITICAL: computeSize変更後は必ずsetSize()を呼び出してレイアウト再計算をトリガー
    const currentSize = [node.size[0], node.size[1]];
    node.setSize(currentSize);
    node.setDirtyCanvas(true, true);

    // CRITICAL: Canvas再描画を複数回トリガーして確実に反映させる
    debugLog(`[LayoutUpdate] Triggering multiple canvas redraws for visual update`);
    requestAnimationFrame(() => {
        node.setSize(currentSize);
        node.setDirtyCanvas(true, true);
        requestAnimationFrame(() => {
            node.setSize(currentSize);
            node.setDirtyCanvas(true, true);
        });
    });

    // リサイズガードを解除 + onResizeを呼び出してレイアウト全体を更新
    setTimeout(() => {
        node._easyscripter_resizing = false;
        debugLog(`[LayoutUpdate] Resize guard released`);

        // ComfyUIのレイアウトシステム全体に変更を伝播
        if (node.onResize) {
            node.onResize(node.size);
        }

        // 最終的なCanvas再描画を追加トリガー
        requestAnimationFrame(() => {
            node.setDirtyCanvas(true, true);
            debugLog(`[LayoutUpdate] Final canvas redraw triggered`);
        });
    }, UI_CONFIG.timing.resizeGuardDelay);

    debugLog(`[LayoutUpdate] Layout updated: outputHeight=${outputHeight}px, scriptHeight=${scriptWidget?.inputEl?.style.height}`);
}

// ========================================
// ノード初期化ヘルパー関数
// ========================================

/**
 * スクリプトウィジェットを設定
 * @param {Object} node - ComfyUIノード
 * @param {Object} scriptWidget - スクリプトウィジェット
 */
function configureScriptWidget(node, scriptWidget) {
    if (!scriptWidget || !scriptWidget.inputEl) return;

    // 初期高さ計算
    const initialNodeHeight = node.size?.[1] || UI_CONFIG.node.defaultHeight;
    const inputSocketArea = calculateInputSocketAreaHeight(node);
    const initialAvailableHeight = initialNodeHeight - inputSocketArea;
    const initialScriptHeight = Math.max(
        UI_CONFIG.widgets.script.minHeight,
        Math.floor(initialAvailableHeight * UI_CONFIG.layout.scriptAreaRatio)
    );

    // スタイル適用（可読性向上）
    applyWidgetStyles(scriptWidget.inputEl, {
        minHeight: initialScriptHeight,
        maxHeight: initialScriptHeight + UI_CONFIG.widgets.script.maxHeightExtra,
        backgroundColor: "#1e1e1e",
        color: "#e0e0e0",  // コントラスト向上
        resize: "vertical",
        isOutput: false  // スクリプトエリア用のフォントサイズ/行間
    });

    // ログエリアとスクリプトエリアの間にスペースを追加（30px → 20px → 23pxに変更：3px下に移動）
    scriptWidget.inputEl.style.marginTop = '23px';

    // computeSize関数を固定値に設定
    scriptWidget.computeSize = function(width) {
        return [width, UI_CONFIG.widgets.script.computeSizeHeight];
    };

    // 親ノード参照を保存
    scriptWidget.parentNode = node;

    // ユーザー手動resize検知: MutationObserverでstyle.height変更を監視
    const resizeObserver = new MutationObserver((mutations) => {
        for (const mutation of mutations) {
            if (mutation.type === 'attributes' && mutation.attributeName === 'style') {
                // ノードのonResize中でない場合、ユーザー操作と判定
                if (!node._easyscripter_resizing) {
                    const currentHeight = scriptWidget.inputEl.style.height;
                    if (currentHeight && currentHeight !== '') {
                        debugLog(`[UserResize] Manual resize detected: height=${currentHeight}`);
                        node._user_manually_resized_script = true;
                    }
                }
            }
        }
    });

    resizeObserver.observe(scriptWidget.inputEl, {
        attributes: true,
        attributeFilter: ['style']
    });
}

/**
 * 出力ウィジェットを設定
 * @param {Object} node - ComfyUIノード
 * @param {Object} outputWidget - 出力ウィジェット（INPUT_TYPESで定義済み）
 * @param {string} locale - 言語設定
 */
function configureOutputWidget(node, outputWidget, locale) {
    if (!outputWidget || !outputWidget.inputEl) return;

    // 初期高さ計算（折りたたみ状態を考慮）
    const logState = getLogDisplayState(node);
    const initialOutputHeight = logState === LOG_DISPLAY_STATES.COLLAPSED
        ? UI_CONFIG.widgets.output.collapsedHeight
        : UI_CONFIG.widgets.output.minHeight;

    // スタイル適用（可読性向上）
    applyWidgetStyles(outputWidget.inputEl, {
        minHeight: initialOutputHeight,
        maxHeight: initialOutputHeight + UI_CONFIG.widgets.output.maxHeightExtra,
        backgroundColor: "#252526",  // コントラスト向上
        color: "#d4d4d4",  // コントラスト向上（緑から白系へ）
        readOnly: true,
        isOutput: true  // 出力エリア用のフォントサイズ/行間
    });

    // プレースホルダー設定
    const placeholderText = 'SCRIPT LOG WILL BE HERE ...';
    outputWidget.inputEl.placeholder = placeholderText;

    // プレースホルダーの色を明示的に設定（CSSと同じ緑色）
    outputWidget.inputEl.style.setProperty('color', '#66ff66', 'important');
    // プレースホルダー専用のスタイルをCSSで制御するためのクラスを追加
    outputWidget.inputEl.classList.add('easyscripter-output');

    // computeSize関数を固定値に設定
    outputWidget.computeSize = function(width) {
        return [width, UI_CONFIG.widgets.output.computeSizeHeight];
    };

    // 親ノード参照を保存
    outputWidget.parentNode = node;

    // 折りたたみ機能の設定は遅延初期化で行う（DOM追加後）
    // setupLogToggle(node, outputWidget); // ← 削除
}


/**
 * リサイズハンドラを設定
 * @param {Object} node - ComfyUIノード
 * @param {Object} scriptWidget - スクリプトウィジェット
 */
function setupResizeHandler(node, scriptWidget) {
    const originalOnResize = node.onResize;

    node.onResize = function(size) {
        // リサイズガードで無限ループ防止
        if (node._easyscripter_resizing) {
            debugLog(`[DEBUG] Resize guard active, skipping resize for node ${node.id}`);
            return;
        }

        node._easyscripter_resizing = true;

        if (originalOnResize) {
            originalOnResize.apply(this, arguments);
        }

        // スクリプトウィジェットのサイズを再計算
        if (scriptWidget && scriptWidget.inputEl) {
            const nodeHeight = size[1];
            const inputSocketArea = calculateInputSocketAreaHeight(node);
            const availableHeight = nodeHeight - inputSocketArea;

            // 折りたたみ状態に応じたoutputHeight取得
            const logState = getLogDisplayState(node);
            const outputHeight = logState === LOG_DISPLAY_STATES.COLLAPSED
                ? UI_CONFIG.widgets.output.collapsedHeight
                : UI_CONFIG.widgets.output.minHeight;

            debugLog(`[Resize] logState=${logState}, outputHeight=${outputHeight}px`);

            // LOOP_SUBGRAPH()プレビューウィンドウ対応のscriptHeight計算
            let scriptHeight;

            if (node._has_preview_widgets) {
                // プレビューウィンドウあり: scriptWidgetは最小高さ固定（ユーザーが手動調整可能）
                scriptHeight = UI_CONFIG.widgets.script.minHeight; // 50px
                debugLog(`[Resize] Preview widgets mode: scriptHeight=${scriptHeight}px (fixed)`);
            } else {
                // プレビューウィンドウなし: 残りスペース全体を使用（折りたたみ状態を考慮）
                scriptHeight = Math.max(
                    UI_CONFIG.widgets.script.minHeight,
                    availableHeight - outputHeight - UI_CONFIG.widgets.spacing
                );
                debugLog(`[Resize] Normal mode: scriptHeight=${scriptHeight}px (dynamic, collapsed=${logState === LOG_DISPLAY_STATES.COLLAPSED})`);
            }

            // ユーザーが手動resizeしていない場合、またはLOOP使用時（プレビューウィンドウあり）は、minHeightを更新
            if (!node._user_manually_resized_script || node._has_preview_widgets) {
                scriptWidget.inputEl.style.minHeight = `${scriptHeight}px`;
                debugLog(`[Resize] minHeight updated to ${scriptHeight}px (manual=${node._user_manually_resized_script}, preview=${node._has_preview_widgets})`);
            } else {
                debugLog(`[Resize] minHeight update skipped (user manually resized)`);
            }
            // maxHeightは常に更新（拡大方向の自由度を確保）
            scriptWidget.inputEl.style.maxHeight = `${scriptHeight + UI_CONFIG.widgets.script.maxHeightExtra}px`;
        }

        // ノードを再描画
        this.setDirtyCanvas(true, true);

        // リサイズガードを解除
        setTimeout(() => {
            node._easyscripter_resizing = false;
        }, UI_CONFIG.timing.resizeGuardDelay);
    };
}

/**
 * Configureハンドラを設定（遅延初期化）
 * @param {Object} node - ComfyUIノード
 */
function setupConfigureHandler(node) {
    const originalOnConfigure = node.onConfigure;

    node.onConfigure = function() {
        if (originalOnConfigure) {
            originalOnConfigure.apply(this, arguments);
        }

        debugLog(`onConfigure called for node ${this.id}`);

        // 初回初期化チェック
        if (!node._easyscripter_initialized) {
            debugLog(`Performing delayed initialization for node ${this.id}`);

            // 遅延初期化を実行
            requestAnimationFrame(() => {
                setTimeout(() => {
                    debugLog(`Delayed initialization executing for node ${this.id}`);

                    // ウィジェット位置の検証と修正
                    const outputWidget = node.widgets.find(w => w.name === "output");
                    const scriptWidget = node.widgets.find(w => w.name === "script");

                    if (outputWidget && scriptWidget) {
                        if (!outputWidget.y || outputWidget.y < 0 || isNaN(outputWidget.y)) {
                            debugLog(`Fixing output widget position for node ${node.id}`);

                            const scriptHeight = scriptWidget.computeSize
                                ? scriptWidget.computeSize(node.size[0])[1]
                                : UI_CONFIG.widgets.script.minHeight;
                            outputWidget.y = (scriptWidget.y || 0) + scriptHeight + UI_CONFIG.widgets.spacing;

                            debugLog(`Set output widget y to ${outputWidget.y}`);
                        }

                        // inputElの再チェックと修正
                        if (outputWidget.inputEl) {
                            outputWidget.inputEl.style.position = "relative";
                            outputWidget.inputEl.style.top = "0";
                            outputWidget.inputEl.style.left = "0";

                            // 折りたたみ機能を設定（DOM追加後）
                            if (!node._logToggleInitialized) {
                                debugLog(`[DelayedInit] Setting up log toggle for node ${node.id}`);
                                setupLogToggle(node, outputWidget);
                                updateLayoutForLogState(node);
                                node._logToggleInitialized = true;
                            }
                        }
                    }

                    // ノードを再描画
                    node.setDirtyCanvas(true, true);

                    // 初期化完了フラグを設定
                    node._easyscripter_initialized = true;
                    debugLog(`Initialization complete for node ${node.id}`);

                }, UI_CONFIG.timing.layoutWaitDelay);
            });
        }
    };
}

// ========================================
// UI設定定数
// ========================================

// ログ表示状態定数
const LOG_DISPLAY_STATES = {
    COLLAPSED: 'collapsed',    // 1行表示（折りたたみ）
    EXPANDED: 'expanded'        // 全行表示（展開）
};

const UI_CONFIG = {
    // ノードサイズ設定
    node: {
        defaultWidth: 450,
        defaultHeight: 300,  // テスト用: 600 → 300（初期配置時の高さを300px縮小）
        minWidth: 350,
        minHeight: 300,  // 修正: 150 → 300（ウィジェット最小高さ合計に対応）
    },
    // レイアウト設定
    layout: {
        // 入力ソケットエリア設定（旧: headerSpace）
        inputSocketAreaMin: 80,            // 入力ソケットエリア最小値（ソケット数が少ない場合）
        inputSocketAreaMax: 250,           // 入力ソケットエリア最大値（ソケット数が多い場合）
        socketHeight: 20,                  // 各ソケットの高さ（ComfyUIデフォルト）
        socketSpacing: 5,                  // ソケット間スペース
        nodeHeaderHeight: 30,              // ノードヘッダー高さ
        scriptAreaRatio: 0.65,             // スクリプトエリア比率（65%）
        outputAreaRatio: 0.35,             // 出力エリア比率（35%）
    },
    // ウィジェット設定
    widgets: {
        script: {
            minHeight: 50,             // LOOP_SUBGRAPH()プレビューウィンドウ対応: ユーザー手動調整可能
            maxHeightExtra: 100,       // minHeightに追加する値
            // ComfyUIレイアウトシステム用の固定高さ報告値
            // ComfyUIはcomputeSizeの戻り値を合計してノード全体の高さを計算する
            // CRITICAL: spacing(30px)がDOM計算で既にカウントされているため、
            // computeSizeHeightの合計にspacingを含める必要がある
            // 診断ログ実測値: 154px (DOM) → 174px (154 + spacing按分20px)
            computeSizeHeight: 174,
        },
        output: {
            minHeight: 200,            // 開いた状態の高さ（100→200に2倍化）
            maxHeightExtra: 100,       // minHeightに追加する値（50→100に2倍化）
            collapsedHeight: 53,       // 折りたたみ時の高さ（80の2/3に縮小）
            // ComfyUIレイアウトシステム用の固定高さ報告値
            // ComfyUIはcomputeSizeの戻り値を合計してノード全体の高さを計算する
            // CRITICAL: spacing(30px)がDOM計算で既にカウントされているため、
            // computeSizeHeightの合計にspacingを含める必要がある
            // 診断ログ実測値: 80px (DOM) → 90px (80 + spacing按分10px)
            computeSizeHeight: 90,
        },
        spacing: 30,                   // ウィジェット間スペース（ログエリアとスクリプトエリアの間のスペース）
    },
    // スタイリング設定
    styling: {
        fontSize: 14,                  // スクリプトエリアのフォントサイズ（可読性向上）
        outputFontSize: 13,            // 出力エリアのフォントサイズ
        padding: 8,
        margin: 5,
        lineHeight: 1.6,               // スクリプトエリアの行間（可読性向上）
        outputLineHeight: 1.5,         // 出力エリアの行間
        widthAdjustment: 10,           // calc(100% - Npx)のN値
    },
    // タイミング設定
    timing: {
        resizeGuardDelay: 100,         // リサイズガード解除までの遅延（ミリ秒）
        layoutWaitDelay: 100,          // レイアウト計算待ち遅延（ミリ秒）
        toggleTransition: 200,         // 折りたたみアニメーション時間（ミリ秒）
    },
    // デバッグ設定
    debug: {
        enabled: true,                 // デバッグログの有効/無効
        substringLength: 100,          // ログ出力時の文字列切り取り長
    },
    // ログ表示設定
    logDisplay: {
        stateProp: 'logDisplayState',  // node.propertiesのプロパティ名
        defaultState: LOG_DISPLAY_STATES.COLLAPSED,  // デフォルト状態（初回ロード時は閉じた状態）
    }
};

// CSSファイルの読み込み
const link = document.createElement('link');
link.rel = 'stylesheet';
link.type = 'text/css';
link.href = './extensions/comfyUI_u5_easyscripter/comfyui_u5_easyscripter.css';
document.head.appendChild(link);

app.registerExtension({
    name: "comfyUI_u5_easyscripter",

    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        // comfyUI_u5_easyscripterノードに対応
        if (nodeData.name === "comfyUI_u5_easyscripter") {
            debugLog(`Registering UI extensions for ${nodeData.name}`);
            
            // ノードが作成されたときの処理
            const onNodeCreated = nodeType.prototype.onNodeCreated;

            nodeType.prototype.onNodeCreated = function() {
                const r = onNodeCreated ? onNodeCreated.apply(this, arguments) : undefined;

                debugLog(`Node created: ${this.type}, ID: ${this.id}`);

                // 言語設定をノードに保存
                const locale = getUserLocale();
                this.properties = this.properties || {};
                this.properties.locale = locale;
                debugLog(`Detected locale: ${locale}`);

                // ノードのリファレンスを保存
                const node = this;

                // 初期化フラグを設定
                node._easyscripter_initialized = false;
                node._easyscripter_resizing = false;
                node._has_preview_widgets = false;      // LOOP_SUBGRAPH()プレビューウィンドウ検知用
                node._preview_widget_count = 0;         // プレビューウィンドウ数
                node._user_manually_resized_script = false;  // ユーザー手動resize検知用

                // 初期ノードサイズ設定（CRITICAL: ウィジェット設定より前に実行）
                this.size = this.size || [UI_CONFIG.node.defaultWidth, UI_CONFIG.node.defaultHeight];
                this.minSize = [UI_CONFIG.node.minWidth, UI_CONFIG.node.minHeight];

                // 出力ウィジェットを設定（INPUT_TYPESで定義済み、1番目）
                const outputWidget = this.widgets.find(w => w.name === "output");
                configureOutputWidget(node, outputWidget, locale);

                // スクリプトウィジェットを設定（INPUT_TYPESで定義済み、2番目）
                const scriptWidget = this.widgets.find(w => w.name === "script");
                configureScriptWidget(node, scriptWidget);

                // リサイズハンドラを設定
                setupResizeHandler(node, scriptWidget);

                // Configureハンドラを設定
                setupConfigureHandler(node);

                // 新規ノード作成時の即座の初期化（onConfigureを待たない）
                requestAnimationFrame(() => {
                    setTimeout(() => {
                        const outputWidget = node.widgets.find(w => w.name === "output");
                        const scriptWidget = node.widgets.find(w => w.name === "script");
                        if (outputWidget && outputWidget.inputEl && !node._logToggleInitialized) {
                            debugLog(`[OnNodeCreated] Setting up log toggle for node ${node.id}`);
                            setupLogToggle(node, outputWidget);
                            updateLayoutForLogState(node);
                            node._logToggleInitialized = true;

                            // DIAGNOSTIC: 余白の原因を特定するための診断ログ
                            setTimeout(() => {
                                const nodeHeight = node.size[1];
                                const inputSocketArea = calculateInputSocketAreaHeight(node);
                                const scriptOffsetHeight = scriptWidget?.inputEl?.offsetHeight || 0;
                                const outputOffsetHeight = outputWidget?.inputEl?.offsetHeight || 0;
                                const scriptComputeSize = scriptWidget?.computeSize(node.size[0])[1] || 0;
                                const outputComputeSize = outputWidget?.computeSize(node.size[0])[1] || 0;

                                const totalWidgetHeight = scriptOffsetHeight + outputOffsetHeight + UI_CONFIG.widgets.spacing;
                                const totalComputeSize = scriptComputeSize + outputComputeSize;
                                const expectedNodeHeight = inputSocketArea + totalComputeSize;
                                const whitespace = nodeHeight - inputSocketArea - totalWidgetHeight;

                                console.log("=== DIAGNOSTIC: Whitespace Analysis ===");
                                console.log(`Node Height: ${nodeHeight}px`);
                                console.log(`Input Socket Area: ${inputSocketArea}px`);
                                console.log(`Script Offset Height: ${scriptOffsetHeight}px`);
                                console.log(`Output Offset Height: ${outputOffsetHeight}px`);
                                console.log(`Script computeSize: ${scriptComputeSize}px`);
                                console.log(`Output computeSize: ${outputComputeSize}px`);
                                console.log(`Total Widget Height (DOM): ${totalWidgetHeight}px`);
                                console.log(`Total computeSize: ${totalComputeSize}px`);
                                console.log(`Expected Node Height: ${expectedNodeHeight}px`);
                                console.log(`Whitespace: ${whitespace}px`);
                                console.log(`Difference (computeSize - DOM): script=${scriptComputeSize - scriptOffsetHeight}px, output=${outputComputeSize - outputOffsetHeight}px`);
                                console.log("=====================================");
                            }, 200);
                        }
                    }, 50);
                });

                return r;
            };

            // 実行結果を受け取ったときの処理
            const onExecuted = nodeType.prototype.onExecuted;

            nodeType.prototype.onExecuted = function(message) {
                debugLog(`onExecuted called for ${this.type} node ${this.id}`, message);
                debugLog(`[DEBUG] Node ID: ${this.id}, Message structure:`, JSON.stringify(message, null, 2));

                const r = onExecuted ? onExecuted.apply(this, arguments) : undefined;

                // 現在の言語設定を取得
                const locale = this.properties?.locale || getUserLocale();

                // 出力ウィジェットを探す
                const outputWidget = this.widgets.find(w => w.name === "output");

                if (outputWidget) {
                    // 【FIX】messageにtextプロパティがない場合（UI出力抑制）は早期リターン
                    if (!message || message.text === undefined) {
                        debugLog(`[DEBUG] No text in message, skipping UI update for node ${this.id}`);
                        return r;
                    }

                    // メッセージを解析して表示用テキストに変換
                    let outputText = parseExecutionMessage(message);

                    // メッセージを翻訳
                    outputText = translateMessage(outputText, locale);

                    debugLog(`Setting output text for ${this.type} node ${this.id}:`, outputText);
                    debugLog(`[DEBUG] outputText length: ${outputText.length} chars`);
                    debugLog(`[DEBUG] Current outputWidget.value: ${outputWidget.value?.substring(0, UI_CONFIG.debug.substringLength)}...`);

                    // ウィジェットに値を設定
                    outputWidget.value = outputText;

                    // inputElがある場合は直接設定も試みる
                    if (outputWidget.inputEl) {
                        debugLog(`[DEBUG] Setting inputEl.value, current height: ${outputWidget.inputEl.style.height}`);
                        outputWidget.inputEl.value = outputText;
                        // スタイルを再適用
                        outputWidget.inputEl.style.backgroundColor = "#2d2d30";
                        outputWidget.inputEl.style.color = "#66ff66";
                    }
                    
                    // ウィジェットの更新を強制
                    if (outputWidget.callback) {
                        outputWidget.callback(outputText);
                    }
                } else {
                    debugLog(`Output widget not found for ${this.type} node ${this.id}`);
                }

                // LOOP_SUBGRAPH()プレビューウィンドウ追加検知
                const expectedWidgets = 2; // script + output
                const currentWidgets = this.widgets.length;

                if (currentWidgets > expectedWidgets && !this._has_preview_widgets) {
                    debugLog(`[EasyScripter] Preview widgets detected: ${currentWidgets - expectedWidgets} widgets added`);
                    this._has_preview_widgets = true;
                    this._preview_widget_count = currentWidgets - expectedWidgets;

                    // レイアウト再計算をトリガー（非同期で実行）
                    requestAnimationFrame(() => {
                        if (this.onResize) {
                            debugLog(`[EasyScripter] Triggering layout recalculation for preview widgets`);
                            this.onResize(this.size);
                        }
                    });
                }

                return r;
            };
        }
    }
});

// 画像プレビュー機能は無効化されています
// EasyScripterノードは画像生成を行わないため、プレビューは不要です
