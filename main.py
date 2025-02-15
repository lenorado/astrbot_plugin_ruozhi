from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
import requests

@register("rz_message", "Your Name", "一个随机返回贴吧段子的插件", "1.0.0", "repo url")
class RandomTiebaMessagePlugin(Star):
   def __init__(self, context: Context):
       super().__init__(context)
       self.api_url = "http://api.yujn.cn/api/tieba.php"

   @filter.command("rz")
   async def rz(self, event: AstrMessageEvent, msg="弱智"):
       '''这是一个随机返回贴吧段子的指令'''
       response = requests.get(self.api_url, params={"type": "json", "msg": msg})
       if response.status_code == 200:
           data = response.json()
           message = f"昵称: {data['name']}\n时间: {data['time']}\n标题: {data['title']}\n内容: {data['text']}\n链接: {data['url']}"
           yield event.plain_result(message)
       else:
           yield event.plain_result("无法获取贴吧段子，请稍后再试。")