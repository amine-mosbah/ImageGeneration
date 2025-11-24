# 🎨 Example Prompts & Tips

A collection of example prompts to help you get started with image generation.

## 📝 Basic Text-to-Image Prompts

### Landscapes

```
a serene mountain landscape at sunset, dramatic clouds
a tropical beach with crystal clear water and palm trees
a misty forest with rays of sunlight breaking through the trees
a snowy mountain peak under northern lights
a desert oasis with sand dunes and a small lake
```

### Architecture

```
a modern glass skyscraper in a futuristic city
an ancient castle on a hilltop surrounded by fog
a cozy wooden cabin in the mountains
a traditional Japanese temple in autumn
a Victorian mansion with intricate details
```

### Characters

```
a wise old wizard with a long beard and magical staff
a friendly robot with glowing blue eyes
a medieval knight in shining armor
an elegant woman in a flowing red dress
a cute cartoon fox character
```

### Fantasy & Sci-Fi

```
a dragon flying over a medieval castle
a spaceship landing on an alien planet
a magical forest with glowing mushrooms
a cyberpunk street with neon signs at night
an enchanted library filled with floating books
```

### Animals

```
a majestic lion with a golden mane
a colorful parrot in a tropical rainforest
a wolf howling at the full moon
a pod of dolphins jumping in the ocean
a red panda sleeping on a tree branch
```

## 🎭 Style-Specific Examples

### Realistic Photography Style

```
a professional portrait of a businesswoman, studio lighting, 8k
a close-up macro photograph of a butterfly on a flower
a landscape photograph of Yosemite Valley at golden hour
an architectural photograph of a modern building at dusk
```

### Anime Style

```
anime girl with long blue hair and magical powers
shounen protagonist with spiky hair wielding a sword
cute chibi character with big eyes
mecha robot in battle pose, detailed mechanical design
```

### Oil Painting Style

```
still life with fruit and wine in the style of Renaissance masters
portrait of a noble woman, classical art style
landscape with rolling hills and farmhouses
stormy seascape with crashing waves
```

### 3D Render Style

```
cute 3D character design, Pixar style
futuristic vehicle concept, detailed 3D model
isometric room interior, cozy bedroom
low poly landscape with geometric trees
```

### Cyberpunk Style

```
rain-soaked street with holographic advertisements
cyborg character with mechanical enhancements
flying cars in a neon-lit megacity
hacker in a dark room surrounded by screens
```

## 💡 Prompt Engineering Tips

### 1. Be Specific

❌ "a house"
✅ "a Victorian-style house with white walls and a red roof, surrounded by a garden"

### 2. Add Quality Modifiers

Add words like:

- "detailed"
- "high quality"
- "professional"
- "8k"
- "masterpiece"
- "award winning"

### 3. Describe Lighting

- "soft lighting"
- "dramatic lighting"
- "golden hour"
- "studio lighting"
- "volumetric lighting"
- "backlit"

### 4. Specify Camera/View

- "close-up portrait"
- "wide angle shot"
- "aerial view"
- "isometric perspective"
- "from below"
- "panoramic"

### 5. Add Artistic References

- "in the style of [artist name]"
- "concept art"
- "trending on artstation"
- "digital painting"
- "illustration"

### 6. Use Weights (Emphasis)

Some models support emphasis:

- "(keyword)" - slight emphasis
- "((keyword))" - more emphasis
- "[keyword]" - de-emphasis

## 🖼️ Image-to-Image Tips

### Strength Settings Guide

**0.1 - 0.3**: Minimal changes

- Color grading
- Slight style tweaks
- Minor detail enhancement
- "adjust colors to be warmer"
- "add slight bloom effect"

**0.4 - 0.6**: Moderate transformation

- Style transfer
- Artistic filters
- Mood changes
- "convert to watercolor painting"
- "make it look like a comic book"

**0.7 - 0.9**: Heavy transformation

- Complete style changes
- Major composition changes
- "transform into a cyberpunk scene"
- "turn into anime style"

**0.9 - 1.0**: Near complete regeneration

- Only rough composition remains
- Almost like text-to-image
- "completely reimagine as fantasy art"

### Good Image-to-Image Prompts

```
turn this into a watercolor painting with soft colors
make it look like a vintage photograph from the 1970s
convert to anime style with vibrant colors
add dramatic storm clouds and lightning
make it look like a professional movie poster
transform into a pencil sketch drawing
add magical glowing effects and particles
convert to pixel art, 16-bit style
make it look like an oil painting by Van Gogh
turn into a futuristic cyberpunk version
```

## 🎯 Advanced Techniques

### Combining Concepts

```
a steampunk airship over a Victorian city, detailed mechanical design, dramatic lighting, concept art
portrait of a wizard-scientist in a magical laboratory filled with glowing potions and futuristic equipment
```

### Specifying Multiple Details

```
a cozy coffee shop interior, wooden furniture, warm lighting, plants by the window, books on shelves, rain outside, afternoon ambiance, highly detailed
```

### Scene Description

```
epic fantasy battle scene: knight on horseback charging through a misty battlefield, castle in background, dramatic sky, cinematic composition, trending on artstation
```

## ⚙️ Parameter Recommendations

### For Portraits

- Steps: 35-50
- Guidance: 7-9
- Resolution: 512x512 or 512x768

### For Landscapes

- Steps: 30-40
- Guidance: 7-10
- Resolution: 768x512 or 768x768

### For Detailed Scenes

- Steps: 40-60
- Guidance: 8-12
- Resolution: 768x768

### For Quick Tests

- Steps: 15-20
- Guidance: 7
- Resolution: 384x384 or 512x512

## 🚫 Common Pitfalls to Avoid

1. **Too vague**: "a thing" → Be specific about what you want
2. **Too complex**: Trying to fit too many concepts in one image
3. **Conflicting descriptions**: "dark night with bright sunny sky"
4. **Expecting exact text**: AI can't reliably generate readable text
5. **Too many characters**: 1-2 characters work best

## 🎪 Fun Experiments

### Mix Unexpected Styles

```
medieval knight in a modern city
ancient Egyptian pharaoh as a cyberpunk character
Renaissance painting of a modern coffee shop
```

### Unusual Combinations

```
a dragon made of flowers and vines
a house built inside a giant tree
floating islands with waterfalls in space
```

### Mood & Atmosphere

```
abandoned amusement park at twilight, eerie atmosphere
cozy library during a thunderstorm, warm lighting
peaceful zen garden at sunrise, minimalist
```

## 📊 Troubleshooting Bad Results

**Image is blurry or low quality?**

- Increase steps to 40-50
- Add quality keywords: "detailed, high quality, sharp, 8k"
- Increase resolution

**Too abstract or weird?**

- Lower guidance scale (try 6-7)
- Be more specific in your prompt
- Use a style preset

**Not matching your prompt?**

- Increase guidance scale (try 10-12)
- Put important keywords at the beginning
- Try different random seeds

**Composition is off?**

- Add composition keywords: "centered, well composed"
- Specify camera angle: "front view", "side view"
- Try multiple generations with different seeds

---

## 🎓 Learning Resources

Want to learn more about prompt engineering?

- Experiment with different combinations
- Keep a prompt library of what works
- Try the same prompt with different styles
- Adjust one parameter at a time to see effects
- Look at prompts that created images you like

---

**Happy generating! 🎨✨**

Remember: The best prompts come from experimentation. Don't be afraid to try unusual combinations!
