# ![image](https://github.com/hongshen-zhang/NeoWizard/assets/51727955/3ba6bf4a-2460-4d1f-98de-5e65e4ec2b2a) 
# Blockchain Math Teacher
## Member : 
| Name  | School                                               | Email | 
| ------------ | --------------- | -------------- | 
| Iris | National University of Singapore                                               | iris921426135@gmail.com |
| Xinjin (Syhthia) Li | Columbia University                                   | li.xinjin@columbia.edu  |
| Hongshen Zhang | Zhejiang University                                 | hongshen.zhang@zju.edu.cn |

       
        

![](https://img.shields.io/badge/License-MIT-lightgrey)
![](https://img.shields.io/badge/Version-v0.0.1-orange)

[NeoWizard](http://118.89.117.111/neopay/)

### For Problem solving
Facilitate an entire process, from capturing math problems via photos to producing automated teaching materials. Its edge over other tools lies in its accuracy and the intelligibility of its answers.

### Advantage of Blockchain
The first user who poses each question **owns the rights to the math lecture notes**. Subsequent identical questions simply call up the pdf and pay the **first user** for access.

![image](https://github.com/hongshen-zhang/NeoWizard/assets/51727955/8909ca45-261d-431b-961f-a594c8455c0f)
![ab3cf8f157bfe5602c8e710ee11aa9c](https://github.com/hongshen-zhang/NeoWizard/assets/51727955/26d9b68d-1f73-4b36-9983-611f658b9465)



## Resource

Deck Link：[NeoWizard](https://docs.google.com/presentation/d/112biul8r-p6cwILilqTb5WUsT9FU2Aya/edit?usp=sharing&ouid=102147246522693605617&rtpof=true&sd=true)

Demo Video Link: [NeoWizard](https://drive.google.com/file/d/1_2itzjz-bNiD3maZFQ1ia5j579MU0f_E/view?usp=sharing)

Website ：[NeoWizard](solvegpt.cn/neopay/)

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
![image](https://github.com/hongshen-zhang/NeoWizard/assets/51727955/932f440f-5402-4c4a-9bea-efa4ee707132)
![image](https://github.com/hongshen-zhang/NeoWizard/assets/51727955/f48ce64e-99e2-4e9c-be7b-4e18b4065b68)
![image](https://github.com/hongshen-zhang/NeoWizard/assets/51727955/67e467cd-0535-44a1-bdbc-e5328dcf0a66)
![image](https://github.com/hongshen-zhang/NeoWizard/assets/51727955/5f059fec-d526-4d4e-92fc-a2fc5664b68e)


## Plan 


| Requirement  | Description                                                 | Time | Progress |
| ------------ | ----------------------------------------------------------- | ---- | -------- |
| Basic Feature | Website launch                                              | July | ✅       |
| Basic Feature | Android version release                                     | Aug  | ✅       |
| Basic Feature | Automatic beamer generation                                 | Aug  | ✅       |
| Basic Feature | Support for Chinese and English, dark mode, different levels| Aug  | ✅       |
| Basic Feature | Launch web3 payment function                                | Aug  | ✅       |
| Patent 1/2   | A method for generating math problem answers based on multi-model adversarial approaches | Sept | ✅       |
| Patent 2/2   | An automated mathematical lecture note generation method based on beamer | Sept | ✅       |
| Code Optimization | Speed up execution                                       | Sept | ❌       |
| Domain Registration | solvegpt.cn                                             | Sept | ✅       |
| Official Launch | Add login function                                         | Oct  | ❌       |


## How to Use:

### Please add the OCR Key and OPENAI Key

```
1. OCR secret key
./solvegpt/main.py line 95:
def tencent_ocr(img_base64):
    cred = credential.Credential(
        "", ""
    )
 
2. OpenAI secret key
./solvegpt/openai_config.json line 2:
{
    "api_key": "",
```



