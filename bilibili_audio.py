import requests
import json
import re
import os

# B站视频BV号
bv_id = "BV1734y1d7m1"

# 获取视频信息的API
api_url = f"https://api.bilibili.com/x/web-interface/view?bvid={bv_id}"

# 发送请求获取视频信息
response = requests.get(api_url)
video_info = response.json()

if video_info['code'] == 0:
    print("获取视频信息成功！")
    print(f"视频标题: {video_info['data']['title']}")
    print(f"视频ID: {video_info['data']['aid']}")
    
    # 获取视频的cid
    cid = video_info['data']['cid']
    print(f"视频CID: {cid}")
    
    # 获取视频的播放信息
    play_api_url = f"https://api.bilibili.com/x/player/playurl?bvid={bv_id}&cid={cid}&qn=120"
    play_response = requests.get(play_api_url)
    play_info = play_response.json()
    
    if play_info['code'] == 0:
        print("获取播放信息成功！")
        # 提取音频URL
        if 'dash' in play_info['data']:
            audio_info = play_info['data']['dash']['audio'][0]
            audio_url = audio_info['baseUrl']
            print(f"音频URL: {audio_url}")
            
            # 下载音频文件
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Referer': f'https://www.bilibili.com/video/{bv_id}'
            }
            
            print("开始下载音频文件...")
            audio_response = requests.get(audio_url, headers=headers, stream=True)
            
            if audio_response.status_code == 200:
                # 保存音频文件
                audio_file_path = "forbidden_rain.mp3"
                with open(audio_file_path, 'wb') as f:
                    for chunk in audio_response.iter_content(chunk_size=1024):
                        if chunk:
                            f.write(chunk)
                print(f"音频文件下载成功，保存为: {audio_file_path}")
            else:
                print(f"下载音频文件失败，状态码: {audio_response.status_code}")
        else:
            print("未找到音频信息")
    else:
        print(f"获取播放信息失败: {play_info['message']}")
else:
    print(f"获取视频信息失败: {video_info['message']}")