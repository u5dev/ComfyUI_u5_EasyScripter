"""
ComfyUI U5 EasyScripter - VBA-style Script Execution Node
"""

from .scripter_node import ComfyUI_u5_EasyScripterNode
from .u5_loaders import (
    u5_CheckpointLoader,
    u5_LoraLoader,
    u5_VAELoader,
    u5_ControlNetLoader,
    u5_CLIPVisionLoader,
    u5_StyleModelLoader,
    u5_GLIGENLoader,
    u5_UNETLoader,
    u5_CLIPLoader,
)

NODE_CLASS_MAPPINGS = {
    "comfyUI_u5_easyscripter": ComfyUI_u5_EasyScripterNode,  # U5シリーズ標準版（INT/FLOAT個別入力）
    # u5 Loader Wrappers - ファイル名出力機能付きローダー
    "u5_CheckpointLoader": u5_CheckpointLoader,
    "u5_LoraLoader": u5_LoraLoader,
    "u5_VAELoader": u5_VAELoader,
    "u5_ControlNetLoader": u5_ControlNetLoader,
    "u5_CLIPVisionLoader": u5_CLIPVisionLoader,
    "u5_StyleModelLoader": u5_StyleModelLoader,
    "u5_GLIGENLoader": u5_GLIGENLoader,
    "u5_UNETLoader": u5_UNETLoader,
    "u5_CLIPLoader": u5_CLIPLoader,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "comfyUI_u5_easyscripter": "ComfyUI U5 EasyScripter",
    # u5 Loader Wrappers
    "u5_CheckpointLoader": "u5 Checkpoint Loader",
    "u5_LoraLoader": "u5 LoRA Loader",
    "u5_VAELoader": "u5 VAE Loader",
    "u5_ControlNetLoader": "u5 ControlNet Loader",
    "u5_CLIPVisionLoader": "u5 CLIP Vision Loader",
    "u5_StyleModelLoader": "u5 Style Model Loader",
    "u5_GLIGENLoader": "u5 GLIGEN Loader",
    "u5_UNETLoader": "u5 UNET Loader",
    "u5_CLIPLoader": "u5 CLIP Loader",
}

WEB_DIRECTORY = "./web"

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS", "WEB_DIRECTORY"]
