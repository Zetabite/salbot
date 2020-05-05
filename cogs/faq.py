import discord
import json
import inspect
import re
import typing
from discord.ext import commands
import datetime
import functools
import logging
logger = logging.getLogger('salc1bot')
automation_logger = logging.getLogger('salc1bot.automated')

def format_timdelta(timdelta):
    total = timdelta.total_seconds()
    minutes = (total//60)%60
    seconds = total%60
    return f"{minutes:.0f}.{seconds:.0f}"

class OnCooldownError(Exception):
    pass
class Cooldown:
    def __init__(self, amount, window, region):
        """
        amount: how often per
        window: minutes
        """
        self.amount = amount
        self.window = datetime.timedelta(minutes=window)
        self.region = region
        self.cooldowns = {}

    def __call__(self, func):
        async def wrapped(*args, **kwargs):
            try:
                id_ = self.region(args, kwargs)
            except Exception as e:
                logger.error(f"Error in cooldown wrapper: {e}")
                return await func(*args, **kwargs)
            last_call = self.cooldowns.get(id_)
            if last_call:
                cooldown_done = last_call + self.window
                now = datetime.datetime.now()
                if cooldown_done > now:
                    delta = cooldown_done - now
                    raise OnCooldownError(f"on cooldown for {format_timdelta(delta)} minutes")
            self.cooldowns[id_] = datetime.datetime.now()
            return await func(*args, **kwargs)
        return wrapped


def FAQMessage_factory(bot, names, regexes, channel_whitelist, message):
    """return cog classes, needed for cog name

    names: List of command names this FAQ Message is known as
    regexes: list of regex r"" strings for matching non-command messages
    channel_whitelist: list of channel ids to respond to
    message: string of the message which the bot responds with
    """

    class FAQMessage(commands.Cog, name=names[0]):
        def __init__(self, bot, names, regexes, channel_whitelist, message,):
            self.bot = bot
            self.names = names
            self.command = commands.command(names[0], aliases=names[1:])(
                self.command_method)  # create the command to be later added to the bot
            self.message = message
            self.regexes = [re.compile(reg) for reg in regexes]
            self.channel_whitelist = channel_whitelist

        @commands.Cog.listener()
        async def on_message(self, message):
            if (not message.author.bot) and (message.author.id != self.bot.user.id) and message.channel.id in self.channel_whitelist and len(message.author.roles) <= 1:
                # check if any of the regexes are matched
                if any(r.search(message.content.lower()) for r in self.regexes):
                    # send the message using the method below
                    try:
                        await self.send(message, message.author, delete_after=30)
                    except OnCooldownError as e:
                        await message.channel.send(f"{e}", delete_after=5)
                    await message.author.send(self.message)
                    automation_logger.info(f"FAQ {self.names[0]} triggered by user {message.author} ({message.author.id}) in {message.channel.name}")
                
        @commands.cooldown(1, 120, commands.BucketType.channel)
        @commands.has_any_role("Member", "Private Chat Access", "OG Role That Has No Purpose", "Moderator", "Administrator")
        async def command_method(self, ctx, member: typing.Optional[discord.Member] = None):
            message = ctx.message
            await message.delete()
            try:
                await self.send(message, member, delete_after=30)
            except OnCooldownError as e:
                await message.channel.send(f"{message.author.mention} {e}", delete_after=5)
                await message.delete()
        
        # this is a seperate method because of the cooldown
        #  amount |  | per minutes 
        @Cooldown(1, 1, lambda args, kwargs: args[2].id)
        async def send(self, message, member,delete_after=45):
            ping = ""
            if member:
                ping += member.mention + "\n"
            # simply send the message
            await message.channel.send(ping + self.message, delete_after=delete_after)

    return FAQMessage(bot, names, regexes, channel_whitelist, message)


def setup(bot):
    channels = [666575359411748875, 666758275504537604,
                660701994549379125, 669119687530905613, 436411303351943188, 548308507636662283]
                # 666575359411748875 = general-pack_png-discussion
                # 666758275504537604 = seed-reverse-engineering
                # REMOVED 666813360867770388 = pack_png-re-creation
                # 660701994549379125 = general chat in cactus uwu's server(testing purposes)
                # 669119687530905613 = not sure?
                # 436411303351943188 = video discussion in sals server
                # 548308507636662283 = general chat in sals server
                

    faq_messages = [
        FAQMessage_factory(
            bot,
            ["dream", "dreams"],
            [r"dream.?s?.?method", ],
            channels,
            ">>> Hey, it looks like you mentioned Dream! Unfortunately we cannot use that method because we don't have enough information."
        ),
        FAQMessage_factory(
            bot,
            ["seed"],
            [r"seed.is.?(?!n)", r"(?:have|know).?the.?seed"],
            channels,
            ">>> Hey, it looks like you mentioned what the seed is! If you actually found the seed, please message a mod. If you're saying this as a joke, please dont :)"
        ),
        FAQMessage_factory(
            bot,
            ["supercomputer", "supercomp", "sc"],
            [r"super.?comput."],
            channels,
            ">>> Hey, it looks like you mentioned a supercomputer! Thankfully `@cactus uwu#0523` is dedicating several supercomputers towards this!"
        ),
        FAQMessage_factory(
            bot,
            ["quantumcomputer", "qcomp", "qc"],
            [r"quantum.?comput."],
            channels,
            ">>> Hey, it looks like you mentioned a quantum computer! Unfortunately this won't help with this problem and we already have enough computing power"
        ),
        FAQMessage_factory(
            bot,
            ["ihelp", ],
            [r"(?:(?:can|may).?i.?help)", r"(do.?to.?help)"],
            channels,
            ">>> Hey, it looks like want to help! If you have reverse-engineering or coding experience head to <#666758275504537604>, otherwise you can help a recreation project in <#666813360867770388>"
        ),
        FAQMessage_factory(
            bot,
            ["notchmessage", "notchmsg", "notch", "built"],
            [r"man.made", r"was built"],
            channels,
            ">>> We have a response from notch, so we dont think its built or a custom seed https://i.vgy.me/zOLSYx.png"
        ),
        FAQMessage_factory(
            bot,
            ["cracked"],
            [r"cracked", r"tlauncher"],
            channels,
            ">>> The anarchy server does NOT allow cracked accounts. Discussion about cracked accounts or account sharing is STRICTLY forbidden"
        ),FAQMessage_factory(
            bot,
            ["hacked"],
            [r"hack"],
            channels,
            ">>> We only talk about utility clients here, please dont mention any \"hacks\". Examples of utility clients include Impact, Future, WWE and Wurst. Also, please do NOT talk about hacking anyone or anything. "
        ),FAQMessage_factory(
            bot,
            ["devs"],
            [r"(ask|email|mojang).*(devs|mojang)"],
            channels,
            ">>> Please don't contact Mojang developers about this. They have already been contacted, and they don't know the seed. https://i.vgy.me/zOLSYx.png"
        ),FAQMessage_factory(
            bot,
            ["tryseed"],
            [r"try.*seed"],
            channels,
            ">>> Hey! Just so you know the seed was randomly generated and it is NOT a word. Also, please don't say its [insert number seed here] because that seed probably wasn't generated. Want to check generation? Use this nice Algorithm! boolean validSeed(long a){long b=18218081,c=1L<<48,d=7847617,e=((((d*((24667315*(a>>>32)+b*(int)a+67552711)>>32)-b*((-4824621*(a>>>32)+d*(int)a+d)>>32))-11)*0xdfe05bcb1365L)%c);return((((0x5deece66dl*e+11)%c)>>16)<<32)+(int)(((0xbb20b4600a69L*e+0x40942de6baL)%c)>>16)==a;}"
        ),FAQMessage_factory(
            bot,
            ["found"],
            [r"(been|have|you|seed).*found.*(seed|)", r"find.*seed", r"(search|searching|hunt).*(active|still|).*(search|seed|).*(seed|)"],
            channels,
            ">>> The seed has not been found yet, and it's currently being searched for! You can look at https://packpng.com/roadmap and https://packpng.com/method for more info!"
        ),FAQMessage_factory(
            bot,
            ["searchall"],
            [r"search.*(every|all).*seed"],
            channels,
            ">>> Searching every seed would take longer than your lifespan, even with very powerful hardware!"
        ),FAQMessage_factory(
            bot,
            ["raiding"],
            [r"raid", r"destroy.*server", r"ruin.*server"],
            channels,
            ">>> Hey! Please don't talk about ruining/destroying/raiding servers! This includes Discord, Minecraft and any other type of server. It's against TOS."
        ),
        
    ]

    for faq in faq_messages:
        bot.add_cog(faq)
        bot.add_command(faq.command)
