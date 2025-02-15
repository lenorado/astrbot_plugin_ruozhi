from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
import requests
import time

# 默认冷却时间为 60 秒
DEFAULT_COOLDOWN = 10

@register("rz_cooldown", "Your Name", "一个带冷却时间的贴吧段子插件", "1.0.0", "repo url")
class RandomTiebaCooldownPlugin(Star):
   def __init__(self, context: Context):
       super().__init__(context)
       self.api_url = "http://api.yujn.cn/api/tieba.php"
       self.cooldown = DEFAULT_COOLDOWN
       self.last_called = {}

   @filter.command("rz")
   async def rz(self, event: AstrMessageEvent, msg="弱智"):
       user_id = event.get_sender_id()
       current_time = time.time()

       # 检查是否有冷却时间
       if user_id in self.last_called and current_time - self.last_called[user_id] < self.cooldown:
           wait_time = self.cooldown - (current_time - self.last_called[user_id])
           yield event.plain_result(f"请等待 {wait_time:.0f} 秒后再试。")
           return

       # 更新最后调用时间
       self.last_called[user_id] = current_time

       response = requests.get(self.api_url, params={"type": "json", "msg": msg})
       if response.status_code == 200:
           data = response.json()
           message = f"昵称: {data['name']}\n时间: {data['time']}\n标题: {data['title']}\n内容: {data['text']}\n链接: {data['url']}"
           yield event.plain_result(message)
       else:
           yield event.plain_result("无法获取贴吧段子，请稍后再试。")

   @filter.command("rzcd")
   async def rzcd(self, event: AstrMessageEvent, seconds: int):
       if seconds > 0:
           self.cooldown = seconds
           yield event.plain_result(f"冷却时间已设置为 {self.cooldown} 秒。")
       else:
           yield event.plain_result("冷却时间必须是一个正整数。")