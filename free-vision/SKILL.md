---
name: free-vision-camera
description: |
  自由视觉 / 自由摄像机 —— 把景别、机位、构图与镜头运动组合成可直接使用的电影化提示词。
  输入场景需求(想拍什么、什么氛围),输出带镜头语言的成片提示词,直接粘贴给视频生成模型
  (MiniMax H3 / Seedance / 可灵 / Wan / LTX 等)。
  支持环绕、推拉、升降、俯仰、FPV、动态跟拍、甩镜等自由摄像机表达。
  触发词:「自由视觉」「自由摄像机」「运镜」「镜头提示词」「分镜运镜」「环绕镜头」「FPV 镜头」
  "camera prompt"、"free camera"、"shot list"。写视频脚本/分镜时同样触发(需要镜头方案时)。
  生成式视频出片(首尾帧/图生视频)时自动附带镜头运动链建议。
---

# 自由视觉 · 自由摄像机(FREE-VISION)

把导演思维翻译成模型听得懂的镜头语言。任何"我要拍 X 画面"的需求,
先给镜头方案(景别 × 机位 × 运动 × 构图),再落成一段可直接粘贴的视频提示词。

## 何时用

- 用户要视频提示词、分镜脚本、镜头方案,尤其提到运镜/机位/景别
- 图生视频、首尾帧连动(记忆:首尾帧须骨骼对应 + 动作链 准备→发力→完成)
- 检查现有提示词为什么"像静态图"(缺运动/缺机位表达)

## 流程

1. 问清:主体是什么、做什么动作、氛围/情绪、时长(默认 5s)、成片比例
   (H3 用 480×832 / 720×1280;像素宽高须为 32 的倍数,720 不行用 704)。
2. 按下面词表拼镜头方案,输出三件套:
   - 景别 + 机位 + 运动(一句话定镜头)
   - 主体动作链(准备→发力→完成,保证首尾帧可连接)
   - 成片提示词(中英文双写,英文段直接给模型)
3. 主动提醒易错点:分辨率 32 倍数、运动幅度别过大(模型易液化)、
   多人物时未指定人物禁止重绘(脸/衣/姿势冻结)。

## 景别词表(从远到近)

| 景别 | 中文 | 提示词 |
|------|------|--------|
| 远景 | 环境为主,人小 | extreme wide shot / wide establishing shot |
| 全景 | 全身入画 | full shot |
| 中景 | 膝上 | medium shot / medium full shot |
| 近景 | 胸上 | medium close-up |
| 特写 | 脸/局部 | close-up / extreme close-up |

## 机位与角度

- 平视 eye level(默认,中性)
- 低机位仰拍 low angle(人物显高大/压迫感)
- 高机位俯拍 high angle(脆弱/全景感)
- 过肩 over-the-shoulder(对话)
- 侧面 profile / 45° 前侧 three-quarter(显轮廓)
- 顶拍 top-down / 底拍 bottom-up(风格化)

## 镜头运动(核心)

| 运动 | 中文 | 提示词 | 用法 |
|------|------|--------|------|
| Push in | 推 | push-in / dolly in | 情绪聚焦,强调 |
| Pull back | 拉 | pull-back / dolly out | 揭示环境/孤独感 |
| Tilt up/down | 俯仰摇 | tilt up / tilt down | 由局部到整体/由整体到局部 |
| Pan | 摇 | pan left/right | 扫视环境 |
| Orbit / revolve | 环绕 | orbit around subject / 360° revolve | 展示主体全貌,动态感最强 |
| Tracking | 跟拍 | tracking shot / follow behind | 动态跟拍,沉浸 |
| Crane / pedestal | 升降 | crane up/down / pedestal up | 史诗感开场/收尾 |
| Handheld | 手持 | handheld / shaky | 纪实、紧张 |
| FPV | 第一人称 | FPV / first-person view / drone view | 穿越感,飞行视角 |
| Whip pan | 甩镜 | whip pan | 转场利器 |

## 构图规则

- 三分法 rule of thirds;引导线 leading lines;对称 symmetry;
  框架构图 frame within frame;留白 negative space;前景遮挡 foreground layers(纵深)。
- 人物视线留白:看向左→人放右。

## 输出模板(直接给模型的英文段)

```
[景别], [主体+动作], [机位/角度], [镜头运动, 速度], [构图], [环境/光线/氛围], [风格], [时长/比例]
```

中文速览一段 + 英文成片一段。用户只要英文就只给英文;只要中文就给中英对照。

## 实例

> 需求:女主在夕阳码头回头,要电影感、镜头绕着她转。
> 镜头方案:近景 × 低机位仰拍 × 环绕 × 三分法留白
> 中文:夕阳下旧码头,穿白裙的女主缓缓回头,发丝被海风吹起;低机位仰拍,
> 镜头以她为圆心匀速环绕 180°,水面反光在背景闪烁;三分构图,右侧留出夕阳
> 逆光剪影;暖金色调,电影胶片质感;5 秒,竖屏。
> 英文:Medium close-up of a woman in a white dress turning her head slowly on a
> weathered pier at sunset, hair blowing in the sea breeze; low angle, the camera
> orbits 180° around her at a steady pace, water glints in the bokeh background;
> rule of thirds with the setting sun rim-lighting her silhouette on the right;
> warm golden grade, cinematic film grain; 5 seconds, 9:16.

## 坑

- 提示词里写"镜头移动"但没说"向哪/多快",模型会乱动 → 运动必须带方向+节奏。
- 环绕超过 360° 或动作幅度太大,人脸/骨骼易变形 → 180° 内 + 动作链收住。
- 首尾帧连动场景:首帧和尾帧人物必须同姿势骨骼起点/终点对应,否则模型只做插值液化。
