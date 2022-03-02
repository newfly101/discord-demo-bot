import discord
from discord.ext import commands
import random

bot = commands.Bot(command_prefix='!')
TOKEN = 'OTQ4NDI4MTQ3ODg2NTM4NzUz.Yh7qiw.KaUjPFDNBk5BY1978y-bx_jQPgo'


@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Game('League of Coding'))
    print('[notice][3rd-party-lib-bot Status Online Success]')


@bot.event
async def on_message(msg):
    if msg.author.bot:
        return None
    await bot.process_commands(msg)


@bot.command()
async def 안녕(ctx):
    print('[notice] 안녕 메세지 출력')
    await bot.change_presence(activity=discord.Game('인사'))
    return await ctx.channel.send(ctx.author.name + '님 하이')


@bot.command()
async def 삭제(ctx):
    LIMIT = 1
    await ctx.channel.purge(limit=LIMIT)
    await ctx.channel.send('메세지를 삭제했습니다.')
    print(f'[notice] limit={LIMIT} 줄 삭제')


@bot.command()
async def 명령어(ctx):
    await bot.change_presence(status=discord.Status.online, activity=discord.Game('설명'))
    embed = discord.Embed(title="명령어 한눈에 보기!!", description="전체 명령어를 미리 준비해놨어요!",
                          color=0x62c1cc)  # Embed의 기본 틀(색상, 메인 제목, 설명)을 잡아줍니다
    embed.add_field(name='> 안녕\r\n', value='따뜻한말 건네드립니다.')
    embed.add_field(name='> 로또\r\n', value='이번 주 추천 로또 번호!')
    embed.add_field(name='> 업데이트\r\n', value='업데이트 일정을 알려드려요!')
    embed.add_field(name='> 홀짝\r\n', value='홀짝 게임(단순무구)\r\nversion 0.1.3')
    embed.set_footer(text="필요하신게 있으시면 요청해 주세요!")
    # await ctx.channel.send(embed=embed)
    await ctx.channel.send("나는 설명 요정이랍니다 ㅎㅎ", embed=embed)


@bot.command()
async def 홀짝(ctx):
    dice = random.randint(1, 6)
    embed = discord.Embed(title='홀, 짝 중에 하나를 선택해주세요', description='선택한 뒤에 어떤 수가 나왔는지 알려드려요.')
    embed.add_field(name='> 주사위의 눈', value='???')
    embed.add_field(name='> 홀수', value='🔴')
    embed.add_field(name='> 짝수', value='🔵')
    await ctx.message.delete()
    msg = await ctx.channel.send(embed=embed)
    await msg.add_reaction('🔴')
    await msg.add_reaction('🔵')
    try:
        def check(reaction, user):
            return str(reaction) in ['🔴', '🔵'] and user == ctx.author and reaction.message.id == msg.id

        reaction, user = await bot.wait_for('reaction_add', check=check)

        if (str(reaction) == '🔴' and dice % 2 == 1) or (str(reaction) == '🔵' and dice % 2 == 0):
            embed = discord.Embed(title='홀, 짝 중에 하나를 선택해주세요', description='정답입니다! 계속해서 도전해보세요!')
        else:
            embed = discord.Embed(title='홀, 짝 중에 하나를 선택해주세요', description='틀렸습니다! 계속해서 도전해보세요!')
        embed.add_field(name='> 주사위의 눈', value=str(dice))
        embed.add_field(name='> 홀수', value='🔴')
        embed.add_field(name='> 짝수', value='🔵')
        await msg.clear_reactions()
        await msg.edit(embed=embed)
    except:
        pass


@bot.command()
async def 업데이트(ctx):
    await ctx.channel.send(f' ' + ctx.author.name + '님 업데이트 소식이 궁금하셨군요!!\r\n' + '최근 업데이트 : 2022-03-02')


@bot.command()
async def 로또(ctx):
    list = []
    while True:
        rotto = random.randint(1, 45)
        if rotto not in list:
            list.append(rotto)
        if len(list) == 6:
            break
        list = sorted(list)
    print(list)
    await bot.change_presence(activity=discord.Game('로또 번호 생성'))
    await ctx.channel.send(f'오늘의 추첨 로또 번호 : {list}')


@bot.command()
async def 얼리기(ctx):
    global isFrozen
    await ctx.message.delete()
    if isFrozen:
        await ctx.channel.send('> 이미 채팅창이 얼어있습니다.')
    else:
        id = ctx.message.author.id
        guild = ctx.message.guild
        member = guild.get_member(id)
        print(f"id:{id}, guild:{guild}, member:{member}")

        permission = 0
        try:
            for role in member.roles:
                if permission < role.position:
                    permission = role.position
        except:
            pass

        if permission >= 3 or guild.owner_id == id:
            # if guild.owner_id == id:
            isFrozen = True
            await ctx.channel.send('> ' + ctx.author.name + '님이 채팅창을 얼렸습니다.')
        else:
            isFrozen = False
            await ctx.channel.send('> ' + ctx.author.name + '님은 권한이 없습니다.')


bot.run(TOKEN)