# я пукну л
import asyncio
from functools import partial

import discord
import json
import mc
import re
from os.path import abspath, dirname
from random import randint

from cogs.Utils import Utils

from discord.ext import commands
from discord.ext.commands import Bot

filepath = dirname(abspath(__file__))

with open(dirname(abspath(__file__)) + '/../data/locales.json') as f:
    locales = json.load(f)

with open(dirname(abspath(__file__)) + '/../data/config.json') as f:
    config = json.load(f)


def get_generated_line(bot, msg, minword=2, maxword=10, minsym=5, maxsym=150):
    samples_txt = mc.util.load_txt_samples(
        filepath + '/../samples/{0}.txt'.format(msg.guild.id), separator="\\")
    generator = mc.StringGenerator(samples=samples_txt)

    result = generator.generate_string(
        attempts=20,
        validator=mc.util.combine_validators(
            mc.validators.words_count(minword, maxword),
            mc.validators.symbols_count(minsym, maxsym),
        ),
    )

    if result == None:
        return 'админ тупой дебил и не смог написать нормальное сооьщение об ошибке, но кароче после 20 попыток сгенерить прикол ниче не получилось, мож быть нету права на чтение сообщений или программист дебил ну в общем держу в курсе'

    else:
        clean_result = re.sub(
            r'''(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))''', "[Link Deleted]", result)

        return clean_result


class TextGen(commands.Cog, name='TextGen'):
    def __init__(self, bot):
        self.bot = bot
        self.name = 'TextGen'

    @ commands.cooldown(1, 5, commands.BucketType.user)
    @ commands.command(aliases=['bugurt'])
    async def b(self, ctx):
        loop = asyncio.get_running_loop()
        lang = Utils.get_lang(None, ctx.message)

        lines = randint(2, 10)
        face = randint(1, 23)
        result = ''

        for _ in range(lines - 1):
            result += (await loop.run_in_executor(None, partial(get_generated_line, self.bot, ctx.message,
                                                                1, 10))).upper() + "\n@\n"

            result += (await loop.run_in_executor(None, partial(get_generated_line, self.bot, ctx.message,
                                                                1, 10))).upper()

        file = discord.File(
            filepath + '/../data/burgut_faces/{0}.jpg'.format(face), filename='{0}.jpg'.format(face))
        embed = discord.Embed(
            color=0xff546b, title=locales[lang]['gen']['burgut_title'], description=result)

        embed.set_image(url='attachment://{0}.jpg'.format(face))
        await ctx.send(file=file, embed=embed)

    @ commands.cooldown(1, 5, commands.BucketType.user)
    @ commands.command(aliases=['dialog', 'dialogue'])
    async def d(self, ctx):
        lang = Utils.get_lang(None, ctx.message)
        loop = asyncio.get_running_loop()

        # try:
        lines = randint(2, 20)

        result = '```'
        for _ in range(lines):
            result += ('> ' + await loop.run_in_executor(None, partial(get_generated_line, self.bot,
                                                                       ctx.message, 1, 10, 5, 150, False))).capitalize() + "\n"
        result += '```'

        embed = discord.Embed(
            color=0xfcf36a, title=locales[lang]['gen']['dialogue_title'], description=result)
        await ctx.send(embed=embed)

        # except Exception:
        #     await ctx.send(embed=Utils.error_embed(locales[lang]['errors']['too_late_gen']))

    # @ commands.cooldown(1, 5, commands.BucketType.user)
    @ commands.command(aliases=['generate', 'g'])
    async def gen(self, ctx, mode=''):
        loop = asyncio.get_running_loop()

        if mode == "1":
            result = await loop.run_in_executor(None, partial(get_generated_line, self.bot, ctx.message, 1, 4))
        elif mode == "2":
            result = await loop.run_in_executor(None, partial(get_generated_line, self.bot, ctx.message, 4, 8))
        elif mode == "3":
            result = await loop.run_in_executor(None, partial(get_generated_line, self.bot, ctx.message, 8, 15))
        else:
            result = await loop.run_in_executor(
                None, partial(get_generated_line, self.bot, ctx.message, 1, 10, 5, 200))

        chance = randint(1, 20)
        if chance >= 1 and chance <= 10:
            result = result.capitalize()
        elif chance >= 11 and chance <= 15:
            result = result.lower()
        elif chance >= 16 and chance <= 20:
            result = result.upper()

        await ctx.send(result)

    @ commands.Cog.listener()
    async def on_message(self, msg):
        if msg.content.startswith('ai.') or msg.content.startswith('aic.'):
            pass
        else:
            # try:
            loop = asyncio.get_running_loop()
            msg_chance = randint(1, 30)
            if msg_chance == 30:
                result = await loop.run_in_executor(None, partial(get_generated_line, self.bot, msg))
                chance = randint(1, 20)
                if chance >= 1 and chance <= 6:
                    result = result.capitalize()
                elif chance >= 7 and chance <= 12:
                    result = result.lower()
                elif chance >= 13 and chance <= 20:
                    result = result.upper()
                await msg.channel.send(result)

            elif '<@!{0}>'.format(self.bot.user.id) in msg.content or '<@{0}>'.format(self.bot.user.id) in msg.content:
                result = await loop.run_in_executor(None, partial(get_generated_line, self.bot, msg))
                chance = randint(1, 20)
                if chance >= 1 and chance <= 5:
                    result = result.capitalize()
                elif chance >= 6 and chance <= 12:
                    result = result.lower()
                elif chance >= 13 and chance <= 20:
                    result = result.upper()
                await msg.channel.send(result)

            else:
                msg_chance = randint(1, 10)
                if msg_chance == 1:
                    for kw in config['keywords']:
                        if kw in msg.content:
                            result = await loop.run_in_executor(None, partial(get_generated_line, self.bot, msg))
                            chance = randint(1, 20)
                            if chance >= 1 and chance <= 5:
                                result = result.capitalize()
                            elif chance >= 6 and chance <= 12:
                                result = result.lower()
                            elif chance >= 13 and chance <= 20:
                                result = result.upper()
                            await msg.channel.send(result)
                            break

            await self.bot.process_commands(msg)

    @ commands.command()
    async def test(self, ctx, *, msg: str):
        clean_result = re.sub(
            r'''(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))''', "[Link Deleted]", msg)
        try:
            mentions = re.findall('\<@!.*?\>', clean_result)
            for mention in mentions:
                clean_mention = re.sub('[<@\!>]', '', mention)
                user = self.bot.get_user(int(clean_mention))
                clean_result = clean_result.replace(
                    mention, f'**\@{user.name}#{user.discriminator}**')
        except:
            pass

        try:
            roles = re.findall('\<@&.*?\>', clean_result)
            for role_mention in roles:
                clean_role_mention = re.sub('[<@&>]', '', role_mention)
                role = discord.utils.get(
                    msg.guild.roles, id=int(clean_role_mention))
                clean_result = clean_result.replace(
                    role_mention, f'**\@{role.name}**')
        except:
            pass

        await ctx.send(clean_result)


def setup(bot):
    bot.add_cog(TextGen(bot))
