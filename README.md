# NeoWizard —— Blockchain Math Teacher

![](https://img.shields.io/badge/License-MIT-lightgrey)
![](https://img.shields.io/badge/Version-v0.0.1-orange)

[NeoWizard](http://118.89.117.111/solvegpt/index.html) 
**Photo input supported**
**More accurate problem-solving**
**Display accuracy rate**
**Automatically generate math lecture notes**

The first user who poses each question **owns the rights to the math lecture notes**. Subsequent identical questions simply call up the pdf and pay the **first user** for access.

![image](https://github.com/hongshen-zhang/NeoWizard/assets/51727955/8909ca45-261d-431b-961f-a594c8455c0f)

## Resource

Demo Video：[NeoWizard](https://www.bilibili.com/video/BV1yj411R7FR/?share_source=copy_web&vd_source=2402ea50d5e761d0c54f9f9cb8f35a85)

Website ：[NeoWizard](http://118.89.117.111/solvegpt/index.html)

Android : [NeoWizard](https://github.com/hongshen-zhang/AI-Math-Teacher/releases/tag/v0.0.1)

Github：[https://github.com/hongshen-zhang/NeoWizard](https://github.com/hongshen-zhang/NeoWizard)


# Demand
1. No Solution for Problem.
![image](https://github.com/hongshen-zhang/NeoWizard/assets/51727955/1503150f-9a30-46a6-9cd7-c2ad5f51a856)
2. Due to unfamiliarity with the relevant theorems, even having the answer doesn't make it understandable.
![image](https://github.com/hongshen-zhang/NeoWizard/assets/51727955/3d78c150-a7c9-451d-a0d2-c661a16bb6d1)
3. Difficulty in sharing problems: NeoWizard allows users to store the problem's pdf on Neo as a personal asset. When accessing the same problem later, it can be directly retrieved, with payment made to the initial creator.
![image](https://github.com/hongshen-zhang/NeoWizard/assets/51727955/17036dbe-3f8f-47aa-864d-9e6b487706d9)


## Spot 
![图片](https://github.com/hongshen-zhang/Unique-hackday_solvegpt/assets/51727955/4ae3cff4-272d-4bcc-b6a9-98a667d89ec1)
![图片](https://github.com/hongshen-zhang/Unique-hackday_solvegpt/assets/51727955/7aff38a8-95d8-42ef-8a6d-453d101fb1c0)
![图片](https://github.com/hongshen-zhang/Unique-hackday_solvegpt/assets/51727955/7777975e-be56-4f78-a2f6-7607d85b3f57)
![图片](https://github.com/hongshen-zhang/Unique-hackday_solvegpt/assets/51727955/5435abf1-5a8f-4285-b4e4-e894bc64de28)

## Plan 计划

目前项目比较早期，也欢迎大家提需求

| 需求         | 描述                                                     | 时间 | 进度 |
| ------------ | -------------------------------------------------------- | ---- | ---- |
| 基本功能     | 网页端上线           | 7 月 | ✅   |
| 基本功能     | 安卓端上限                             | 8 月 | ✅   |
| 基本功能      | 自动生成beamer                  | 8 月 | ✅   |
| 写专利 1/2       | 一种基于多模型对抗的数学问题答案生成方法                   | 8 月 | ✅   |
| 写专利 2/2     | 一种基于beamer的自动化数学课件生成方法              | 8 月 |✅   |
| 基本功能     | 支持中英文，黑暗模式，不同学历              | 8 月 |✅   |
| 基本功能     | 上线web3支付功能                | 8 月 |✅   |
| 代码优化   | 加快运行速度                                 | 9 月 | ❌   |
| 注册域名   | solvegpt.cn                                 | 9 月 | ❌   |
| 正式上线 | 增加登录功能                             | 10 月 | ❌   |


## 使用方法：

### 请补充OCR Key和OPENAI Key

```
1. ocr secret key
./solvegpt/main.py line 95:
def tencent_ocr(img_base64):
    cred = credential.Credential(
        "", ""
    )
 
2. openai secret key
./solvegpt/openai_config.json line 2:
{
    "api_key": "",
```



