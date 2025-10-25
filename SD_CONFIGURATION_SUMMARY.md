# Stable Diffusion Configuration Summary

## ✅ Your Configuration is CORRECT

### Location
```
D:\Nexus\StableDiffusionWebUI\stable-diffusion-webui-master\
```

### Settings (webui-user.bat)
```batch
PYTHON=C:\Users\moonc\AppData\Local\Programs\Python\Python310\python.exe
COMMANDLINE_ARGS= --api
```

✅ **API is enabled** - This is required for Nexus to communicate with SD

---

## Photo Agent Settings

Your Photo Agent is configured with optimal settings:

| Setting | Value | Purpose |
|---------|-------|---------|
| **API URL** | http://localhost:7860 | Standard SD WebUI port |
| **Steps** | 40 | Good quality (20=fast, 40=balanced, 80=slow) |
| **Resolution** | 768x768 | High quality images |
| **CFG Scale** | 8.5 | Strong prompt following |
| **Sampler** | DPM++ 2M Karras | Best quality sampler |
| **Restore Faces** | True | Automatically fixes face issues |
| **Negative Prompt** | Comprehensive | Filters out bad artifacts |

---

## No Changes Needed!

Your Stable Diffusion is already correctly configured. Just make sure:

1. ✅ Run `START_NEXUS.bat` to launch everything
2. ⏱️ Wait 60-90 seconds for SD to fully load
3. 🎨 Then generate images through Nexus

---

## Test Image Generation

Once SD is loaded, try in Nexus:
- "create a kitten playing ukulele on a porch"
- "generate a sunset over mountains"
- "make an image of a futuristic city"

You'll get actual PNG files saved to:
```
D:\AIArm\Generated\Images\nexus_image_XXXXXXXX.png
```

---

## Advanced: Optional Optimizations

If you want even better quality, you can edit `webui-user.bat`:

```batch
set COMMANDLINE_ARGS= --api --xformers --medvram
```

- `--xformers` = Faster generation (requires xformers library)
- `--medvram` = For GPUs with 6-8GB VRAM
- `--lowvram` = For GPUs with 4GB or less

But your current config is perfect for standard use!
