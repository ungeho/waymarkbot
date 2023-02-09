# 環境変数用
import os
# 正規表現
import re
# 計算用
import math
# インストールした discord.py を読み込む
import discord


# Botのアクセストークン 環境変数から
TOKEN = os.environ['WAYMARKBOT_TOKEN']

# 接続に必要なオブジェクトを生成
client = discord.Client()


# 起動時に動作する処理
@client.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    print('ログインしました')

# メッセージ受信時に動作する処理
@client.event
async def on_message(message):
    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return
    # message全削除
    if message.content == "/clear":
        await message.channel.purge()
        await message.channel.send("履歴を全て削除しました。")
    # フィールドマーカーの座標を計算する
    if message.content.startswith("/waymark"):
        # \d+ \d{1,}と同じ、最長一致、最短一致にしたい場合は\d+?
        # (?:) グループ化のみに()を使いたい時に使える。後方参照をしない
        # (?:)? グループ化したものが0or1回
        r_str = re.search(r" [R|r]=(\d+(?:\.\d+)?)", message.content)
        ang_str = re.search(r" (?:Ang|ang|ANG)=(-?\d+(?:\.\d+)?)", message.content)
        if (r_str != None) and (ang_str != None):
            r   = float(r_str.group(1))
            ang = float(ang_str.group(1))
            # await message.channel.send("r   = " + str(r))
            # await message.channel.send("ang = " + str(ang))
            cx_str = re.search(r" (?:CX|cx)=(-?\d+(?:\.\d+)?)", message.content)
            if cx_str != None :
                cx = float(cx_str.group(1))
            else :
                cx = 100
            cy_str = re.search(r" (?:CY|cy)=(-?\d+(?:\.\d+)?)", message.content)
            if cy_str != None:
                cy = float(cy_str.group(1))
            else:
                cy = 0
            cz_str = re.search(r" (?:CZ|cz)=(-?\d+(?:\.\d+)?)", message.content)
            if cz_str != None:
                cz = float(cz_str.group(1))
            else:
                cz = 100
            cir_str = re.search(r" (?:Cir|cir)=(\d)", message.content)
            if cir_str != None:
                cir = int(cir_str.group(1))
            else:
                cir = 1
            param_str =  "以下のパラメーターが設定されました。\n"
            param_str += "```\n"
            param_str += "r = " + str(r) + "\n"
            param_str += "ang = " + str(ang) + "\n"
            param_str += "cx = " + str(cx) + "\n"
            param_str += "cy = " + str(cy) + "\n"
            param_str += "cz = " + str(cz) + "\n"
            param_str += "cir = " + str(cir) + "\n"
            param_str += "```\n"
            await message.channel.send(param_str)
            coord_str = ""
            if cir == 1:
                # x座標の計算
                x = cx + r * math.cos(ang*math.pi/180)
                # z座標の計算
                z = cz - r * math.sin(ang*math.pi/180)
                coord_str = "座標は以下の通りです。\n"
                coord_str += "```\n"
                coord_str += "x = " + str(x) + "\n"
                coord_str += "y = " + str(cy) + "\n"
                coord_str += "z = " + str(z) + "\n"
                coord_str += "```\n"
            else:
                div = 360/cir
                coord_str = "座標は以下の通りです。\n"
                coord_str += "```\n"
                coord_str += "Angle :\t   X   \t   Y   \t   Z   \n"
                for i in range(cir):
                    angi = ang - div*i
                    if angi < 0:
                        angi = 360 + angi
                    # x座標の計算
                    x = cx + r * math.cos(angi*math.pi/180)
                    # z座標の計算
                    z = cz - r * math.sin(angi*math.pi/180)
                    coord_str += "{:6.2f}".format(angi) + ":\t" + "{:7.3f}".format(x) + "\t" + "{:7.3f}".format(cy) + "\t" + "{:7.3f}".format(z) + "\n"
                coord_str += "```\n"
            await message.channel.send(coord_str)
        else:
            await message.channel.send("r ang のどちらかあるいは両方未指定です。")
    # 散開時にAoEが重ならない半径の計算
    if message.content.startswith("/spread"):
        r_str = re.search(r" (?:R|r)=(\d+(?:\.\d+)?)", message.content)
        if r_str != None :
            r = float(r_str.group(1))
            aoer = 6
            aoer_str = re.search(r" (?:AoE|aoe|AOE|Aoe)=(\d+(?:\.\d+)?)", message.content)
            if aoer_str != None :
                aoer = float(aoer_str.group(1))
            people = 8
            people_str = re.search(r" (?:people|People|PEOPLE)=([2-8])", message.content)
            if people_str != None :
                people = int(people_str.group(1))
            param_str =  "以下のパラメーターが設定されました。\n"
            param_str += "```"
            param_str += "r       =" + str(r) + "\n"
            param_str += "AoERange=" + str(aoer) + "\n"
            param_str += "People  =" + str(people) + "\n"
            param_str += "```"
            await message.channel.send(param_str)
            # ２点間の距離
            # div  = 360/people
            # dist = math.sqrt(math.pow(r-r*math.cos(div*math.pi/180),2) + math.pow(r*math.sin(div*math.pi/180),2))
            # 円に内接する正多角形の辺の長さ
            dist = 2.0 * r * math.sin(math.pi/people)
            spread_str = "散開結果\n"
            spread_str += "```"
            spread_str += "Dist <= AoER : AoEが重なる\n"
            spread_str += "Dist >  AoER : AoEが重ならない\n"
            spread_str += "dist = " + str(dist) + "\n"
            spread_str += "AoER = " + str(aoer) + "\n"
            if dist <= aoer:
                spread_str += "Dist <= AoERの為、AoEが重なります。"
            else:
                spread_str += "Dist >  AoERの為、AoEが重なりません"
            spread_str += "```"
            await message.channel.send(spread_str)
        else:
            await message.channel.send("散開する円周の半径rが未指定です。")


# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)