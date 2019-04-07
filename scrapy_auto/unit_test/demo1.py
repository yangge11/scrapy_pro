#!/usr/bin/python
# coding=utf8
# Copyright 2017 SARRS Inc. All Rights Reserved.

# @Time    : 2019/1/25 11:45
# @Author  : zengyang@tv365.net(ZengYang)
# @File    : demo_spider.py
# @Software: PyCharm
# @ToUse  :
import random

from scrapy_auto.tools.common_parser import del_html_attr


def del_html_attr_test():
    page_source = """
    <article class="article" id="mp-editor"> 
 <p data-role="original-title" style="display:none">原标题：全球每37秒就有1个人死于静脉血栓，这2个动作就能避免风险！久坐久站的人一定要学起来！</p> 
 <p style="text-align: center;"><img src="http://5b0988e595225.cdn.sohucs.com/images/20181122/30c1351d5c524cad8524c1f80049388f.jpeg"></p> 
 <p>全球每37秒就有1人死于静脉血栓栓塞性疾病，住院、手术、久坐是高危因素</p> 
 <p><span style="font-size: 16px;">久坐久站人群，试试踝泵运动</span></p> 
 <p>北京大学第三医院心血管内科主管护师 张卨 </p> 
 <p><span style="font-size: 16px;">指导专家</span></p> 
 <p><span style="font-size: 16px;">北京协和医院骨科副主任医师 <span>庄乾宇</span></span></p> 
 <p>编者按 </p> 
 <p style="text-align: justify;"><span style="font-size: 16px;">国际血栓与止血学会提供的资料显示，全球每16秒就有一人患静脉血栓栓塞性疾病，每37秒就有一人死于该病。但更可怕的是，很多时候静脉血栓形成后并无明显症状，一旦血栓脱落，或引起肺部或脑部等地方的栓塞，严重者可在1~2小时死亡，即便度过危险期，仍然存在栓塞复发的风险。</span></p> 
 <p style="text-align: justify;">住院、手术、长期卧床、久坐是高危因素。数据显示，每静坐一个小时，患深静脉血栓形成的风险会增加10%；坐90多分钟，会使膝关节血液循环降低50%。这就意味着那些久坐久站人群，如长时间乘坐飞机、火车或久坐办公室者，也处于风险当中。对于这些人群，不妨在平时多做做踝泵运动。</p> 
 <p style="text-align: justify;">踝泵运动，其实和生活中的勾脚尖和绷脚尖是一样的。踝泵运动是通过踝关节的运动，起到像泵一样的作用，促进下肢的血液循环和淋巴回流。它包括踝关节的屈伸和绕环运动。</p> 
 <p style="text-align: justify;">对于卧床及手术之后患者的功能恢复，有着至关重要的作用。同时它也适用于久坐久站人群，比如长时间乘坐飞机、火车或久坐办公室者，可以预防下肢静脉曲张。</p> 
 <p>踝泵运动的原理 </p> 
 <p style="text-align: justify;">跖屈（绷脚尖）时，小腿三头肌收缩变短，胫骨前肌放松伸长；背伸（勾脚尖）时，胫骨前肌收缩变短，小腿三头肌放松伸长。</p> 
 <p style="text-align: justify;">肌肉收缩时，血液和淋巴液受挤压回流，肌肉放松时，新鲜血液补充。</p> 
 <p style="text-align: justify;">通过这样简单的屈伸脚踝，可以有效促进整个下肢的血液循环。绕环动作原理类似。</p> 
 <p>踝泵运动分为屈伸和绕环两组动作 </p> 
 <p>0<span>1</span></p> 
 <p>屈伸动作 </p> 
 <p style="text-align: center;"><img src="http://5b0988e595225.cdn.sohucs.com/images/20181122/a05fbc9ad25940fb8dbad328cb9a0118.jpeg"></p> 
 <p style="text-align: justify;">您可以躺或坐在床上，下肢伸展，大腿放松，缓缓勾起脚尖，尽力使脚尖朝向自己，至最大限度时保持10秒钟。然后脚尖缓缓下压，至最大限度时保持10 秒钟。然后放松，这样一组动作完成。</p> 
 <p style="text-align: justify;"><span>稍休息后可再次进行下一组动作。反复地屈伸踝关节，最好每个小时练习5分钟，一天练5~8次。</span></p> 
 <p>0<span>2</span></p> 
 <p>绕环动作 </p> 
 <p style="text-align: center;"><img src="http://5b0988e595225.cdn.sohucs.com/images/20181122/d889e99f0981474f944feb9f6d33ffc9.jpeg"></p> 
 <p style="text-align: justify;">您可以躺或坐在床上，下肢伸展，大腿放松，以踝关节为中心，脚趾作360度绕环，尽力保持动作幅度最大。绕环可以使更多的肌肉得到运动。可顺时针和逆时针交替进行。</p> 
 <p>若疼痛剧烈，可只做屈伸动作 </p> 
 <p style="text-align: justify;">由于手术后的长时间静卧，血液循环不畅，肌腱会有不同程度的萎缩，绕环动作的幅度会受限，甚至出现疼痛感。如果体力不够，或疼痛剧烈，只做屈伸动作效果也不错。待疼痛减轻后，再加做绕环动作。</p> 
 <p style="text-align: justify;">刚开始练习时用较小的力量，逐渐适应后再增加强度。练习中如感觉疼痛明显，可减少练习的时间、次数。</p> 
 <p style="text-align: justify;"><span>需要注意的是，踝部术后或石膏固定者不宜进行踝泵练习。</span></p> 
 <p style="text-align: justify;">当然，即使您很健康，我们也建议您，每隔1小时起来活动一下。不要小看这短短的几分钟，这个小小的动作会给您的健康带来大收益。</p> 
 <p style="text-align: right;"><span style="font-size: 16px;">文中图片来自网络 / 编辑 || 李璐</span><a href="//www.sohu.com/?strategyid=00001 " target="_blank" title="点击进入搜狐首页" id="backsohucom" style="white-space: nowrap;"><span class="backword"><i class="backsohu"></i>返回搜狐，查看更多</span></a></p> 
 <p data-role="editor-name">责任编辑：<span></span></p> 
</article>
    """
    aa = del_html_attr(page_source)
    pass


def demo1_AI():
    while True:
        print(input("").replace('吗', '').replace('？', ''))


def random_demo():
    aa = [1, 3, 565, 12, 8, 2]
    a_list = random.shuffle(aa)
    for i in a_list:
        print(i)
    pass


if __name__ == '__main__':
    # del_html_attr_test()
    # demo1_AI()
    random_demo()
