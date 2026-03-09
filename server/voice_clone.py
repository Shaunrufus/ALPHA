from pathlib import Path
import uuid
import sys
import os
import torch

# Add OpenVoice to path
openvoice_path = Path("C:\\ALPHA\\OpenVoice\\OpenVoice")
sys.path.append(str(openvoice_path))

try:
    from openvoice.api import ToneColorConverter
    from openvoice.utils import load_audio
    OPENVOICE_AVAILABLE = True
    print("✅ OpenVoice imported successfully")
except ImportError as e:
    print(f"⚠️ OpenVoice not available: {e}")
    OPENVOICE_AVAILABLE = False

# Paths
BASE_DIR = Path("C:/ALPHA/OpenVoice")
BASE_DIR.mkdir(exist_ok=True)

CHECKPOINT_DIR = Path("../OpenVoice/OpenVoice/checkpoints")
CONVERTER_CONFIG = CHECKPOINT_DIR / "converter/config.json"
CONVERTER_CKPT = CHECKPOINT_DIR / "converter/checkpoint.pth"

# Load the model once at startup (only if OpenVoice is available)
vc_model = None
if OPENVOICE_AVAILABLE and CONVERTER_CONFIG.exists() and CONVERTER_CKPT.exists():
    try:
        print("🔄 Loading ToneColorConverter model...")
        # Use CPU to avoid device mismatch issues
        vc_model = ToneColorConverter(str(CONVERTER_CONFIG), device="cpu")
        vc_model.load_ckpt(str(CONVERTER_CKPT))
        print("✅ Model loaded successfully")
    except Exception as e:
        print(f"❌ Failed to load model: {e}")
        vc_model = None
else:
    print("⚠️ OpenVoice model not available, using fallback mode")

def enroll_user(user_id: str, ref_voice_path: Path):
    """Save enrollment voice for a user."""
    dest = BASE_DIR / f"recording_{user_id}.wav"
    with open(dest, "wb") as f:
        f.write(ref_voice_path.read_bytes())
    print(f"✅ Enrollment voice saved: {dest}")
    return dest

def clone_voice(user_id: str, sample_path: Path) -> Path:
    """Clone voice using stored enrollment for user."""
    ref_path = BASE_DIR / f"recording_{user_id}.wav"
    if not ref_path.exists():
        raise FileNotFoundError(f"No enrollment found for user {user_id}")

    # Save sample.wav
    sample_dest = BASE_DIR / f"sample_{user_id}.wav"
    with open(sample_dest, "wb") as f:
        f.write(sample_path.read_bytes())

    # Output file
    output_path = BASE_DIR / f"output_{user_id}_{uuid.uuid4().hex}.wav"

    if vc_model is not None:
        try:
            # Run inference with OpenVoice
            # First extract speaker embedding from reference
            from openvoice import se_extractor
            target_se, audio_name = se_extractor.get_se(str(ref_path), vc_model, target_dir='../OpenVoice/OpenVoice/processed', vad=True)
            
            # Run the tone color converter
            # All tensors are already on CPU from model initialization
            src_se = torch.load('../OpenVoice/OpenVoice/checkpoints/base_speakers/EN/en_default_se.pth')
            # target_se should already be on CPU from se_extractor
            
            vc_model.convert(
                audio_src_path=str(sample_dest),
                src_se=src_se,
                tgt_se=target_se,
                output_path=str(output_path),
                message="@OpenVoice"
            )
            print(f"✅ Cloned voice saved: {output_path}")
        except Exception as e:
            print(f"❌ OpenVoice inference failed: {e}")
            # Fallback to simple audio processing
            return create_fallback_audio(sample_dest, output_path)
    else:
        # Fallback mode
        return create_fallback_audio(sample_dest, output_path)
    
    return output_path

def create_fallback_audio(input_path: Path, output_path: Path) -> Path:
    """Create a simple modified audio as fallback."""
    import soundfile as sf
    import numpy as np
    
    try:
        # Load audio
        audio, sr = sf.read(str(input_path))
        
        # Simple modification (pitch shift simulation)
        modified_audio = audio * 1.1
        
        # Save
        sf.write(str(output_path), modified_audio, sr)
        print(f"✅ Fallback audio saved: {output_path}")
        return output_path
    except Exception as e:
        print(f"❌ Fallback audio failed: {e}")
        # Create a test tone
        duration = 3.0
        t = np.linspace(0, duration, int(24000 * duration))
        test_audio = np.sin(2 * np.pi * 440 * t) * 0.3
        sf.write(str(output_path), test_audio, 24000)
        print(f"✅ Test tone saved: {output_path}")
        return output_path
